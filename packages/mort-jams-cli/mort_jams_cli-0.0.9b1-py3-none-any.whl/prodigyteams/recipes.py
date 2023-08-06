import json
import tarfile
from pathlib import Path
from zipfile import ZipFile

import typer

from . import packages
from .utils import (
    dicts_to_table,
    normalize_module,
    printer,
)

# TODO: Test all this if this approach works correctly

app = typer.Typer()


@app.callback()
def recipes():
    """
    Sub-commands for recipes.
    """


@app.command()
def new(
    name: Path = typer.Argument(
        ..., help="Recipes package name, e.g. custom_recipes", exists=False
    ),
    version: str = typer.Option(
        "0.1.0", help="The version of the Python package with the recipes"
    ),
    description: str = typer.Option("", help="Python package description"),
    author: str = typer.Option("", help="Python package author"),
    email: str = typer.Option("", help="Python package author email"),
    url: str = typer.Option("", help="Python package URL"),
    licence: str = typer.Option("", help="Python package license"),
):
    """
    Generate a new Prodigy Teams Recipe directory with a custom package.
    """
    package_name = normalize_module(name.name)
    package_path = name / package_name
    package_path.mkdir(parents=True)
    setup_path = name / "setup.py"
    setup_path.write_text(TEMPLATE_SETUP, encoding="utf-8")
    init_path = package_path / "__init__.py"
    init_path.write_text(TEMPLATE_INIT, encoding="utf-8")
    recipes_path = package_path / "recipes.py"
    recipes_path.write_text(TEMPLATE_RECIPES, encoding="utf-8")
    meta_path = package_path / "meta.json"
    meta_data = {
        "name": package_name,
        "version": version,
        "description": description,
        "author": author,
        "email": email,
        "url": url,
        "license": licence,
        "type": "prodigy_teams_recipes",
        "prodigy_teams_recipes": {},
    }
    meta_path.write_text(json.dumps(meta_data, indent=4), encoding="utf-8")
    printer.good(f"Successfuly created project {name.name}")
    printer.divider("venv")
    printer.info("Now you can enter that directory and create a new venv, e.g. with")
    printer.info("$ python3 -m venv env")
    printer.info(
        "Then activate it, and make sure you install prodigy_teams_recipes from your Prodigy Teams cluster"
    )
    printer.info(
        "Also make sure you install setuptools and wheel if you don't have them already in your environment, e.g."
    )
    printer.info("$ pip install setuptools wheel")
    printer.divider("Edit")
    printer.info(f"You can edit the custom recipes at {recipes_path.resolve()}")
    printer.info(
        f"If you add new recipes modules (Python files), make sure you import them at {init_path.resolve()}"
    )
    printer.divider("Publish")
    printer.info("After you are done, you can build your recipes with:")
    printer.info("$ python setup.py sdist bdist_wheel")
    printer.info(
        "This will update the required meta.json file right before building the package"
    )
    printer.info(
        "Then you can upload your recipes package with the CLI subcommand: recipes add"
    )


@app.command()
def verify(
    package: Path = typer.Argument(
        ..., help="The recipes package file to verify", exists=True, dir_okay=False
    )
):
    """
    Verify a Prodigy Teams Recipe built Python package before upload.
    """
    if not (package.name.endswith("tar.gz") or package.name.endswith(".whl")):
        printer.fail(
            "It seems this is not a Python package, it should end in .tar.gz or .whl"
        )
        raise typer.Abort()
    file_name = ""
    meta_json = None
    valid_meta = False
    if package.name.endswith(".whl"):
        with ZipFile(package) as zip_file:
            for file_name in zip_file.namelist():
                if file_name.endswith("/meta.json"):
                    meta_bytes = zip_file.read(file_name)
                    meta_json = json.loads(meta_bytes.decode("utf-8"))
                    if not isinstance(meta_json, dict):
                        continue
                    if meta_json.get("type") == "prodigy_teams_recipes":
                        valid_meta = True
                        break
    elif package.name.endswith(".tar.gz"):
        with tarfile.open(package) as tar:
            for file_name in tar.getnames():
                if file_name.endswith("/meta.json"):
                    io_bytes = tar.extractfile(file_name)
                    assert io_bytes
                    meta_json = json.load(io_bytes)
                    if not isinstance(meta_json, dict):
                        continue
                    if meta_json.get("type") == "prodigy_teams_recipes":
                        valid_meta = True
                        break
    if not (valid_meta and meta_json):
        printer.fail("No valid meta.json found in packaage")
        raise typer.Exit(1)
    printer.good(f"Found valid meta.json in package: {file_name}")
    recipes_data = meta_json.get("prodigy_teams_recipes", {})
    if not isinstance(recipes_data, dict):
        printer.fail("Invalid meta.json key prodigy_teams_recipes")
        raise typer.Exit(1)
    if not recipes_data:
        printer.fail(
            "No custom recipes found, make sure you install prodigy_teams_recipes and prodigy in your venv, and then make sure you run python setup.py sdist bdist_wheel"
        )
        raise typer.Exit(1)
    recipes_info = []
    valid_recipes = True
    for key, data in recipes_data.items():
        entry_point = data.get("entry_point")
        recipe_schema = data.get("recipe_schema")
        recipes_info.append(
            {
                "name": key,
                "entry_point": entry_point,
                "contains schema": bool(recipe_schema),
            }
        )
        if not entry_point or not recipe_schema:
            valid_recipes = False
    headers, rows = dicts_to_table(recipes_info)
    printer.good("Custom recipes found!")
    printer.table(rows, header=headers, divider=True, max_col=3000)
    if not valid_recipes:
        printer.fail("One or more recipes are not valid")
        raise typer.Exit(1)
    printer.good("Valid recipes package!")


@app.command()
def add(package: typer.FileBinaryRead, allowoverwrite: bool = False):
    """
    Add/upload a recipe package from the local filesystem.

    It should be a valid file in your local file system,
    it will also be validated and indexed by your broker's Python Package Index.
    """
    package_path = Path(package.name)
    verify(package=package_path)
    packages.add(package=package, allowoverwrite=allowoverwrite)


TEMPLATE_SETUP = """
#!/usr/bin/env python3
import importlib
import json
from pathlib import Path

from setuptools import find_packages, setup


def update_meta(*, package_name: str, meta: dict, meta_path: Path):
    try:
        importlib.import_module(package_name)
        from prodigy_scale_recipes.decorator import get_custom_meta
        custom_meta = get_custom_meta()
        meta.update(custom_meta)
        meta_path.write_text(json.dumps(meta, indent=4), encoding="utf-8")
    except ModuleNotFoundError:
        # Probably installing from sdist, not building
        pass


def get_meta_path():
    root = Path(__file__).parent.resolve()
    meta_path = None
    for sub_path in root.iterdir():
        if sub_path.is_dir():
            meta_path = sub_path / "meta.json"
            if meta_path.is_file():
                break
    assert meta_path
    return meta_path


def setup_package():
    meta_path = get_meta_path()
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    package_name = meta["name"]
    update_meta(package_name=package_name, meta=meta, meta_path=meta_path)
    recipes: dict = meta["prodigy_teams_recipes"]
    recipe_entry_points = []
    for recipe_name, recipe_data in recipes.items():
        recipe_entry_point = recipe_data["entry_point"]
        recipe_entry_points.append(f"{recipe_name} = {recipe_entry_point}")

    setup(
        name=package_name,
        description=meta.get('description'),
        author=meta.get('author'),
        author_email=meta.get('email'),
        url=meta.get('url'),
        version=meta['version'],
        license=meta.get('license'),
        packages=find_packages(),
        package_data={package_name: ["meta.json"]},
        install_requires=[
            "prodigy_scale_recipes>=0.0.5<0.0.6"
        ],
        zip_safe=False,
        entry_points={
            "prodigy_teams_recipes": recipe_entry_points
        },
    )


if __name__ == "__main__":
    setup_package()
""".lstrip()


TEMPLATE_RECIPES = """
from prodigy_scale_recipes.decorator import scale_recipe
from prodigy_scale_recipes.schemas import Recipe


class CustomRecipe(Recipe):
    class Config:
        title = "A Sample Custom Recipe"


@scale_recipe("custom_recipe")
def custom_recipe(recipe: CustomRecipe):
    return {
        "view_id": "classification",
        "dataset": recipe.dataset,
        "stream": ["Hello World from custom recipe"],
    }
""".lstrip()


TEMPLATE_INIT = """
from . import recipes
""".lstrip()
