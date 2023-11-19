import asyncio
import click

from src.bot.main import main as bot
from src.services.import_data import ImportDataService
from src.services.commands import Commands
from src.settings import BASE_DIR


@click.group()
def cli():
    pass


@cli.command()
def run_bot():
    asyncio.run(bot())


@cli.command()
@click.argument("patch", type=click.Path(exists=True), required=True)
def write_programs(patch: str):
    asyncio.run(ImportDataService().import_file(path=(BASE_DIR / patch)))


@cli.command()
@click.argument("username", type=click.STRING, required=True)
@click.argument("password", type=click.STRING, required=True)
def create_staff(username: str, password: str):
    asyncio.run(Commands.create_staff(username, password))
    click.echo(f"User {username} created")


if __name__ == "__main__":
    cli()
