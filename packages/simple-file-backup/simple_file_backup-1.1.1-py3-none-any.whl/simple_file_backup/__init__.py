import os
import re
import json
import asyncio
import sqlite3
import argparse
from shutil import SameFileError
from shutil import copyfile
from datetime import datetime
from datetime import timedelta

__version__ = "1.1.1"


class SimpleFileBackup:
    TIMESTAMP_FORMAT = "%Y%m%dT%H%M%SZ"

    def __init__(
        self,
        file_path,
        backup_directory_path,
        prefix="backup",
        extension=".bak",
        backup_config=[
            {"dirname": "hourly", "period": 1, "limit": 48},
            {"dirname": "daily", "period": 24, "limit": 14},
            {"dirname": "weekly", "period": 168, "limit": 12},
            {"dirname": "every30days", "period": 720, "limit": float("inf")},
        ],
        backup_method="copy",
    ):
        self.BACKUP_METHODS = {
            "copy": self.file_copy_backup,
            "sqlite3": self.sqlite3_backup,
        }

        if not file_path or not backup_directory_path:
            return

        if re.search(r"[^A-Za-z0-9_\-]", prefix) is not None:
            raise ValueError(
                "Base name must only contain ASCII letters, numbers, "
                "underscore and hyphen"
            )
        if re.search(r"[^A-Za-z0-9_\-\.]", extension) is not None:
            raise ValueError(
                "Extension must only contain ASCII letters, numbers, "
                "underscore, hyphen and dot"
            )
        if not os.path.exists(file_path):
            raise ValueError("Source file does not exist")
        if not os.path.exists(backup_directory_path):
            raise ValueError("Destination backup directory does not exist")
        if not isinstance(backup_config, list):
            raise TypeError("Backup period definition must be a list of dicts")
        if len(backup_config) < 1:
            raise ValueError("Must provide at least 1 backup period")
        for backup in backup_config:
            if (
                len(backup) != 3
                or "dirname" not in backup
                or "period" not in backup
                or "limit" not in backup
            ):
                raise KeyError("Wrong key(s) in backup period definition")
            if (
                not isinstance(backup["dirname"], str)
                or re.search(r"[^A-Za-z0-9_\-]", backup["dirname"]) is not None
            ):
                raise ValueError(
                    "Backup period dirname name must be a string containing only"
                    "ASCII letters, numbers, underscore and hyphen"
                )
            if (
                not isinstance(backup["period"], int)
                and not isinstance(backup["period"], float)
                or backup["period"] <= 0
            ):
                raise TypeError(
                    "Backup period must either be a positive (non-zero) int or float"
                )
            if backup["limit"] == "inf":
                backup["limit"] = float("inf")  # allow "inf" for file limit
            if (
                not isinstance(backup["limit"], int)
                and backup["limit"] != float("inf")
                or backup["limit"] <= 0
            ):
                raise TypeError(
                    "Backup period file limit must be a positive (non-zero) int or inf"
                )
        if extension[0] != ".":
            extension = "." + extension
        if backup_method not in self.BACKUP_METHODS:
            raise ValueError(
                "Backup method must be one of "
                f"{[key for key in self.BACKUP_METHODS]}"
            )

        self.file_path = file_path
        self.backup_directory_path = backup_directory_path
        self.prefix = prefix
        self.extension = extension
        self.backup_config = backup_config
        self.backup_method = backup_method

    def __getattribute__(self, name):
        if name == "new_file_name":
            return "{}-{}{}".format(
                self.prefix,
                datetime.utcnow().strftime(self.TIMESTAMP_FORMAT),
                self.extension,
            )
        return super().__getattribute__(name)

    @staticmethod
    def _exception_handler(loop, context):
        # first, handle with default handler
        loop.default_exception_handler(context)
        # stop the loop
        loop.stop()

    @staticmethod
    def file_copy_backup(source, target):
        copyfile(source, target)

    @staticmethod
    def sqlite3_backup(source, target):
        source_conn = sqlite3.connect(f"file:{source}?mode=ro", uri=True)
        target_conn = sqlite3.connect(target)
        source_conn.backup(target_conn, pages=1, sleep=0.025)

    def directory_status(self, directory):
        backup_files = [
            file_name
            for file_name in os.listdir(directory)
            if re.search(
                r"{}\-\d\d\d\d\d\d\d\dT\d\d\d\d\d\dZ$".format(self.prefix),
                os.path.splitext(file_name)[0],
            )
            is not None
        ]
        if len(backup_files) > 0:
            latest = backup_files[-1]
            latest_time = datetime.strptime(
                os.path.splitext(latest)[0].rpartition("-")[2], self.TIMESTAMP_FORMAT,
            )
        else:
            latest = None
            latest_time = None

        return {
            "latest": latest,
            "latest_time": latest_time,
            "num_backups": len(backup_files),
            "list": backup_files,
        }

    async def create_backup(self, max_backups, period, dirname=None):
        full_directory_path = os.path.join(self.backup_directory_path, dirname)
        if dirname is not None:
            if not os.path.exists(full_directory_path):
                os.mkdir(full_directory_path)
        directory = (
            self.backup_directory_path
            if dirname is None
            else os.path.join(self.backup_directory_path, dirname)
        )
        while True:
            status = self.directory_status(directory)
            if status["latest"] is None or (
                datetime.utcnow() - status["latest_time"]
            ) >= timedelta(hours=period):
                try:
                    self.BACKUP_METHODS[self.backup_method](
                        self.file_path, os.path.join(directory, self.new_file_name)
                    )
                    print("simple-file-backup: ", end="")
                    print(
                        f"created {os.path.join(directory, self.new_file_name)} "
                        f"({self.backup_method})"
                    )
                except FileNotFoundError:
                    print("simple-file-backup: ", end="")
                    print("warn: source file '{}' not found".format(self.file_path))
                except PermissionError:
                    print("simple-file-backup: ", end="")
                    print(
                        "warn: permission denied copying file '{}' to '{}'".format(
                            self.file_path, os.path.join(directory, self.new_file_name),
                        )
                    )
                except SameFileError:
                    # this really shouldn't happen
                    print("simple-file-backup: ", end="")
                    print("warn: source and destination files are the same")
                num_files_to_delete = status["num_backups"] + 1 - max_backups
                if num_files_to_delete < 0:
                    num_files_to_delete = 0
                for i in range(num_files_to_delete):
                    try:
                        os.remove(os.path.join(full_directory_path, status["list"][i]))
                    except FileNotFoundError:
                        print("simple-file-backup: ", end="")
                        print(
                            "warn: file '{}' vanished before deletion".format(
                                os.path.join(full_directory_path, status["list"][i])
                            )
                        )
                    except PermissionError:
                        print("simple-file-backup: ", end="")
                        print(
                            "warn: permission denied deleting file '{}'".format(
                                os.path.join(full_directory_path, status["list"][i])
                            )
                        )

            await asyncio.sleep(1)

    def create_tasks(self, loop):
        for backup_setting in self.backup_config:
            loop.create_task(
                self.create_backup(
                    backup_setting["limit"],
                    backup_setting["period"],
                    backup_setting["dirname"],
                )
            )

    def run(self):
        loop = asyncio.get_event_loop()
        loop.set_exception_handler(self._exception_handler)
        self.create_tasks(loop)
        loop.run_forever()


def cmdline():
    try:
        parser = argparse.ArgumentParser(
            prog="simple-file-backup",
            description="Console application for periodically backing up a single "
            "file.",
            usage="%(prog)s FILE BACKUP_DIR [-ext EXT] [-conf CONF] [-method METHOD]",
        )
        parser.add_argument("file_path", help="path of file to back up")
        parser.add_argument(
            "backup_dir_path", help="path of the directory for the backups"
        )
        parser.add_argument(
            "-ext",
            default=".bak",
            help="file extension of the backups; default is '.bak'",
        )
        parser.add_argument(
            "-prefix",
            default="backup",
            help="backup file name prefix; default is 'backup'",
        )
        parser.add_argument(
            "-conf",
            metavar="FILE",
            help="path to an optional config file that defines the backup intervals, "
            "subdirectories and file limits; by default hourly, daily, weekly and "
            "30-day interval backups are created with 48, 14, 12 and unlimited number "
            "of files respectively",
        )
        parser.add_argument(
            "-method",
            default="copy",
            help="backup method; the default is 'copy' (simple file copy), for sqlite3 "
            "database files, use 'sqlite3' to avoid corrupting the backups",
        )
        args = parser.parse_args()

        # parse backup periods config file
        backup_config = None
        if args.conf:
            if os.path.exists(args.conf):
                try:
                    backup_config = json.load(open(args.conf))
                except Exception:
                    parser.print_usage()
                    print("simple-file-backup: error: config JSON file is malformed")
                    exit()
            else:
                parser.print_usage()
                print("simple-file-backup: error: config file does not exist")
                exit()

        try:
            simple_backup = SimpleFileBackup(
                args.file_path,
                args.backup_dir_path,
                args.prefix,
                args.ext,
                backup_config=[
                    {"dirname": "hourly", "period": 1, "limit": 48},
                    {"dirname": "daily", "period": 24, "limit": 14},
                    {"dirname": "weekly", "period": 168, "limit": 12},
                    {"dirname": "every30days", "period": 720, "limit": float("inf")},
                ]
                if backup_config is None
                else backup_config,
                backup_method=args.method,
            )
            print(
                "simple-file-backup: creating backups of '{}' in '{}'".format(
                    simple_backup.file_path, simple_backup.backup_directory_path
                )
            )
            print(
                "simple-file-backup: backup prefix is '{}', extension is '{}'".format(
                    simple_backup.prefix, simple_backup.extension
                )
            )
            for backup_setting in simple_backup.backup_config:
                print(
                    "simple-file-backup: backing up in dirname '{}' every {} "
                    "hour(s), limit {}".format(
                        backup_setting["dirname"],
                        backup_setting["period"],
                        backup_setting["limit"],
                    )
                )
            print("simple-file-backup: started.")
            simple_backup.run()
        except Exception as e:
            parser.print_usage()
            print("simple-file-backup: error: {}".format(e.args[0]).lower())
            exit()

    except KeyboardInterrupt:
        print("simple-file-backup: stopped (aborted).")
