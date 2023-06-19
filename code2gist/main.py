import argparse
import json
import os
import textwrap

import pathspec
import requests


def create_gist(description, files):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("❌ GITHUB_TOKEN environment variable not found")
    url = "https://api.github.com/gists"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {"public": False, "description": description, "files": files}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 201:
        error_message = response.text
        # Parse the error message JSON
        try:
            error_json = json.loads(error_message)
            if "errors" in error_json:
                for error in error_json["errors"]:
                    if (
                        "code" in error
                        and error["code"] == "missing_field"
                        and "field" in error
                        and error["field"] == "files"
                    ):
                        # A more friendly error message
                        error_message = "No files found to create a gist. Check your .code2gistignore file or use the --ext option to specify file extensions to include."
        except json.JSONDecodeError:
            pass  # If the error message is not valid JSON, leave it as is
        print(f"❌ Failed to create a gist: {error_message}")
        return None
    return response.json()


def _load_ignore_file(directory, filename):
    file_path = os.path.join(directory, filename)
    ignore_spec = None
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            ignore_spec = pathspec.PathSpec.from_lines("gitwildmatch", f)
    else:
        if filename == ".code2gistignore":
            with open(file_path, "w") as f:
                pass  # create an empty .code2gistignore file
    return ignore_spec


def _valid_file(filename, rel_path, extensions, gitignore, code2gistignore):
    if not any(filename.endswith(ext) for ext in extensions):
        return False
    if gitignore and gitignore.match_file(rel_path):
        return False
    if code2gistignore and code2gistignore.match_file(rel_path):
        return False
    return True


def get_files_in_directory(directory, extensions):
    gitignore = _load_ignore_file(directory, ".gitignore")
    code2gistignore = _load_ignore_file(directory, ".code2gistignore")

    files = {}
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            path = os.path.join(root, filename)
            rel_path = os.path.relpath(path, directory)
            if not _valid_file(
                filename, rel_path, extensions, gitignore, code2gistignore
            ):
                continue

            try:
                with open(path, "rt", encoding="utf-8") as file:
                    files[rel_path] = {"content": file.read()}
            except (UnicodeDecodeError, IOError) as e:
                print(f"❌ Error reading file: {path}. Error: {str(e)}")
    return files


def delete_old_gists():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("❌ GITHUB_TOKEN environment variable not found")
    url = "https://api.github.com/gists"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to fetch gists: {response.text}")
        return
    gists = response.json()

    deleted_gists = []
    failed_gists = []

    for gist in gists:
        if "[code2gist]" in gist["description"]:
            delete_url = f"https://api.github.com/gists/{gist['id']}"
            delete_response = requests.delete(delete_url, headers=headers)
            if delete_response.status_code != 204:
                print(
                    f"❌ Failed to delete Gist: {gist['id']}, response: {delete_response.text}"
                )
                failed_gists.append(gist["id"])
                continue
            deleted_gists.append(gist["id"])

    print("\n" + "=" * 100)
    print("🌳  Pruned Gists 🌳".center(100))
    print()

    wrapper = textwrap.TextWrapper(width=99, subsequent_indent=" " * 12)

    if deleted_gists:
        for gist in deleted_gists:
            print("\n".join(wrapper.wrap(f"{' '*5}✔️   {gist}")))
        print()

    if failed_gists:
        print("-" * 100)
        print("❌ Failed Gists ❌".center(100))
        for gist in failed_gists:
            print("\n".join(wrapper.wrap(f"{' '*5}✖️   {gist}")))
        print()

    print("=" * 100 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Upload Python files in a directory to Gist."
    )
    parser.add_argument(
        "directory", type=str, nargs="?", help="the directory to upload"
    )
    parser.add_argument(
        "--ext", nargs="+", default=[".py"], help="file extensions to include"
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="delete all gists created by this application",
    )
    args = parser.parse_args()

    response = None  # define response before checking args.directory

    if args.directory:
        directory = args.directory
        description = os.path.basename(os.getcwd()) + " [code2gist]"
        files = get_files_in_directory(directory, args.ext)
        response = create_gist(description, files)

    if response:
        wrapper = textwrap.TextWrapper(width=99, subsequent_indent=" " * 12)

    print("\n" + "=" * 100)
    print("📂  Gist URL 📂".center(100))
    print()
    print("\n".join(wrapper.wrap(f"{'🌐 URL:'.ljust(10)} {response['html_url']}")))
    print()
    print("-" * 100)
    print("📄  File URLs 📄".center(100))
    for filename, file_info in response["files"].items():
        print(f"\n{'📁 File:'.ljust(10)} {filename}")
        print(f"{'🌐 URL:'.ljust(10)} {file_info['raw_url']}")
    print("=" * 100 + "\n")

    if args.prune:
        delete_old_gists()


if __name__ == "__main__":
    main()
