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
        print(f"❌ Failed to create a gist: {response.text}")
        return None
    return response.json()


def get_files_in_directory(directory, extensions):
    # Load the .gitignore file, if it exists.
    gitignore_path = os.path.join(directory, ".gitignore")
    gitignore = None
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            gitignore = pathspec.PathSpec.from_lines("gitwildmatch", f)

    files = {}
    for root, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if not any(filename.endswith(ext) for ext in extensions):
                continue
            path = os.path.join(root, filename)
            rel_path = os.path.relpath(path, directory)

            # Skip the file if it matches a .gitignore rule.
            if gitignore and gitignore.match_file(rel_path):
                continue

            try:
                with open(path, "rt", encoding="utf-8") as file:
                    files[rel_path] = {"content": file.read()}
            except (UnicodeDecodeError, IOError) as e:
                print(f"❌ Error reading file: {path}. Error: {str(e)}")
                continue
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
            url_parts = file_info["raw_url"].split("/raw", 1)
            print(f"{'🌐 URL:'.ljust(10)} {url_parts[0]}")
            print(" " * 12 + "/raw" + url_parts[1])
        print("=" * 100 + "\n")

    if args.prune:
        delete_old_gists()


if __name__ == "__main__":
    main()
