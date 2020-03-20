"""An exploration of the tool for builing CLIs. Greatly simplifies the scripting

Can install the package (https://typer.tiangolo.com/) as `pip install typer`. 
Note, that for autocompletion we have to write more code or publish the package.
"""

from typing import List, Dict, Tuple, Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel

from pathlib import Path
import typer

import items  # another dummy module

# =================== CLI Package Metadata ======================
# ===============================================================
__version__ = "0.1.1"
existing_usernames = ["rick", "morty"]
state = {"verbose": False}

class Membership(str, Enum):
    payg = "payg"
    vip = "vip"

def version_callback(value: bool):
    """A callback to return the version number of the tool"""
    if value:
        typer.echo(f"Welcome to the CLI world: {__version__}")
        raise typer.Exit()


app = typer.Typer(help="An awesome CLI user manager.")
app.add_typer(items.app, name="items")


# =================== Very basic commands =======================
# ===============================================================
@app.command("hello")
def hello(name: str):
    """
    Greet a person. `python main.py hello Mihai`
    """
    typer.echo(f"Hello {name}!")


@app.command("bye", help="Just a goodbye!")
def goodbye(name: str, formal: bool = False):
    """
    Say goodbye in a formal or informal way.
    """
    if formal:
        typer.secho(
            f"Goodbye Mr. {name}. Have a good day!",
            fg=typer.colors.GREEN, bold=True
        )
    else:
        # otherwise would have to do style |> echo
        typer.secho(
            f"Goodbye  {name}!", fg=typer.colors.RED # bg=typer.colors.RED
        )


# =========== Absolutely fake usesr registration ================
# ===============================================================
def maybe_create_user(username: str, role: str):
    """
    Helper function to print stuff and control flow for an user
    """
    if username in existing_usernames:
        typer.secho("The user already exists", fg=typer.colors.RED)
        raise typer.Exit(code=0)
    elif username == "root":
        typer.secho("The root user is reserved", underline=True)
        raise typer.Exit(code=1) # Can also use typer.Abort()
    else:
        typer.echo(f"User created: {username}")
        typer.echo(f"User has the role of a: {role}")


def send_new_user_notification(username: str):
    """
    Helper to fake out a user notification
    """
    typer.echo(f"Notification sent for new user: {username}")


def role_callback(value: str) -> str:
    """
    A callback for validating a role. Non-Wizards are not allowed
    """
    typer.secho(f"Validating the role.")
    if value != "Wizard":
        raise typer.BadParameter("Only Wizards are allowed!")
    return value


# =========== The main command for user registration ============
# ===============================================================
@app.command("register")
def flow(
    username: str = typer.Argument(...), 
    role: str = typer.Argument("Wizard", callback=role_callback),

    country: str = typer.Option(
        ..., "--country", "-c", prompt=True, help="Country of residence?"
    ),
    birthday: datetime = typer.Option(..., formats=["%Y-%m-%d"]),
    terms: bool = typer.Option(
        ..., "--agree/--reject", "-t", confirmation_prompt=True, 
        help="T&Conditions", prompt="Do you agree to the terms and conditions?"
    ),
    password: str = typer.Option(...,
        prompt=True, confirmation_prompt=True, hide_input=True
    ),
    home: bool = typer.Option(True, help="Home right now?", show_default=True),
    version: bool = typer.Option(
        None, "--version", "-v", callback=version_callback, is_eager=True
    ),
    membership: Membership = typer.Option(...)
) -> None:
    """
    Fake out a user registration flow. Register with USERNAME, 
    Usage example: python main.py flow Mihai DataScientist --home true
    """
    maybe_create_user(username=username, role=role)
    send_new_user_notification(username=username)
    typer.secho(f"Is at home: {home}")

    if state["verbose"]:
        typer.echo(f"Some kind of error. VEEERY VERBOSE.", err=True)
        typer.echo(birthday)


@app.callback()
def main(verbose: bool=False):
    """
    Manage users in the CLI app
    """
    typer.echo("""
        ======= Patience, trying to register ========
        =============================================
    """)
    if verbose:
        typer.echo("Will write verbose output")
        state["verbose"] = True


# =========== Working with files and paths as inputs ============
# ===============================================================
@app.command("read")
def read_file(
    config: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    )
):
    """
    typer.FileText [FileTextWrite|FileBinaryRead|FileBinaryWrite] 
    can also be very useful for working with files typer.Option(mode="a")
    """
    text = config.read_text()
    typer.echo(f"Config file contents: {text}")


# =========== Progress bars and UX ==============================
# ===============================================================
@app.command("work")
def progressbar():
    import time
    total = 0
    with typer.progressbar(range(100)) as progress:
        for value in progress:
            # Fake processing time
            time.sleep(0.01)
            total += 1
    typer.echo(f"Processed {total} things.")


if __name__ == "__main__":
    app()