import logging.config
import asyncio
import click

from src.bot.main import main as bot
from src.services.import_data import ImportDataService
from src.services.commands import Commands
from src.settings import BASE_DIR, LOGGING_CONFIG


@click.group()
def cli():
    pass


@cli.command()
def run_bot():
    """Run application"""
    logging.config.dictConfig(LOGGING_CONFIG)
    bot()


@cli.command()
@click.argument("patch", type=click.Path(exists=True), required=True)
def write_programs(patch: str):
    """Writing data from a file"""
    asyncio.run(ImportDataService().import_file(path=(BASE_DIR / patch)))


@cli.command()
@click.argument("username", type=click.STRING, required=True)
@click.argument("password", type=click.STRING, required=True)
def create_user_staff(username: str, password: str):
    """Create user with permission staff"""
    asyncio.run(Commands.create_user_staff(username, password))
    click.echo(f"User {username} [staff] created")


@cli.command()
@click.argument("username", type=click.STRING, required=True)
@click.argument("password", type=click.STRING, required=True)
def create_superuser(username: str, password: str):
    """Create user with permission superuser"""
    asyncio.run(Commands.create_superuser(username, password))
    click.echo(f"User {username} [superuser] created")


if __name__ == "__main__":
    cli()
