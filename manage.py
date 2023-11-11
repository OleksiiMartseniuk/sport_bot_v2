import asyncio
import click

from src.bot.main import main as bot
from src.services.import_data import ImportDataService
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


if __name__ == "__main__":
    cli()
