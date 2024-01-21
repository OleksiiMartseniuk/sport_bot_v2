import glob
import subprocess
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv


load_dotenv()


DB_HOST = os.getenv("POSTGRES_HOST")
DB_USER = os.getenv("POSTGRES_USER")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

BACKUP_PATH = os.getenv("BACKUP_PATH")

FILENAME_PREFIX = "sport_bot_v2.backup"
FORMAT_DATA = "%Y_%m_%d_%H_%M"
NOW = datetime.now()


def create_backup():
    filename = f"{NOW.strftime(FORMAT_DATA)}-{FILENAME_PREFIX}"
    destination = f"{BACKUP_PATH}/{filename}"

    print(f"Backing up {DB_NAME} database to {destination}")
    subprocess.Popen((
        "pg_dump "
        f"--host={DB_HOST} "
        f"--username={DB_USER} "
        f"--no-password "
        f"--dbname={DB_NAME} "
        "-Fc "
        f"--file={destination}"),
        env=dict(PGPASSWORD=DB_PASSWORD),
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )


def remove_backup(count_day: int = 7):
    date_remove = NOW - timedelta(days=count_day)

    for file in glob.glob(f"{BACKUP_PATH}/*.backup"):
        date_file_str = file.split("/")[-1].split("-")[0]
        date_file = datetime.strptime(date_file_str, FORMAT_DATA)
        if date_file.date() < date_remove.date():
            os.remove(file)


def main():
    create_backup()
    remove_backup()


if __name__ == "__main__":
    main()
