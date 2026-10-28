import argparse
from pathlib import Path

STARTER_FILES = {
    "README.md": "# Practical Assignment\n\n## Aim\n\n## Procedure\n\n## Output\n",
    "main.py": '"""Main file for this practical."""\n\n\ndef main():\n    print("Practical started successfully.")\n\n\nif __name__ == "__main__":\n    main()\n',
    "notes.txt": "Practical notes:\n",
}


def create_practical(name, dry_run=False, verbose=False):
    folder = Path(name)

    if folder.exists():
        print(f"Error: '{name}' already exists.")
        return 1

    if folder.is_absolute() or ".." in folder.parts or len(folder.parts) != 1:
        print("Error: Enter a folder name, not a path.")
        return 1

    planned = [folder / filename for filename in STARTER_FILES]

    if dry_run:
        print(f"Dry run: {folder}/")
        for path in planned:
            print(f"  Would create: {path}")
        print("No files or folders were changed.")
        return 0

    try:
        folder.mkdir()
        for filename, content in STARTER_FILES.items():
            path = folder / filename
            path.write_text(content, encoding="utf-8")
            if verbose:
                print(f"Created: {path}")

        print(f"Practical folder created: {folder}")
        print(f"Created {len(STARTER_FILES)} starter files.")
        return 0

    except OSError as error:
        print(f"Error creating practical: {error}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        prog="pracflow",
        description="Create standard practical assignment folders and files."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser(
        "create", help="Create a practical folder and starter files"
    )
    create_parser.add_argument("name", help="Name of the practical folder")
    create_parser.add_argument(
        "-n", "--dry-run", action="store_true",
        help="Preview changes without creating anything"
    )
    create_parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Show each created file"
    )

    list_parser = subparsers.add_parser(
        "list", help="List practical folders in the current directory"
    )
    list_parser.add_argument(
        "directory", nargs="?", default=".",
        help="Directory to inspect (default: current directory)"
    )

    args = parser.parse_args()

    if args.command == "create":
        raise SystemExit(
            create_practical(args.name, args.dry_run, args.verbose)
        )

    if args.command == "list":
        directory = Path(args.directory)
        if not directory.is_dir():
            parser.error(f"Not a directory: {directory}")
        folders = sorted(
            item.name for item in directory.iterdir()
            if item.is_dir()
        )
        if folders:
            print("\n".join(folders))
        else:
            print("No folders found.")
        return


if __name__ == "__main__":
    main()