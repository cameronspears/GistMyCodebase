import argparse
import json
import os

import pathspec
import requests


def create_gist(description, files):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not found")
    url = "https://api.github.com/gists"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {
        "public": False,
        "description": description,
        "files": files
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 201:
        print(f"Failed to create a gist: {response.text}")
        return None
    return response.json()

def get_files_in_directory(directory, extensions):
    # Load the .gitignore file, if it exists.
    gitignore_path = os.path.join(directory, '.gitignore')
    gitignore = None
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            gitignore = pathspec.PathSpec.from_lines('gitwildmatch', f)

    files = {}
    for root, dirnames, filenames in os.walk(directory):
        dirnames[:] = [d for d in dirnames if d[0] != '.']
        for filename in filenames:
            if filename.startswith('.') or not any(filename.endswith(ext) for ext in extensions):
                continue
            path = os.path.join(root, filename)
            rel_path = os.path.relpath(path, directory)

            # Skip the file if it matches a .gitignore rule.
            if gitignore and gitignore.match_file(rel_path):
                continue

            try:
                with open(path, 'rt') as file:
                    files[rel_path] = {"content": file.read()}
            except (UnicodeDecodeError, IOError) as e:
                print(f"Error reading file: {path}. Error: {str(e)}")
                continue
    return files

def delete_old_gists():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not found")
    url = "https://api.github.com/gists"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch gists: {response.text}")
        return
    gists = response.json()
    for gist in gists:
        if '[code2gist]' in gist['description']:
            delete_url = f"https://api.github.com/gists/{gist['id']}"
            delete_response = requests.delete(delete_url, headers=headers)
            if delete_response.status_code != 204:
                print(f"Failed to delete Gist: {gist['id']}, response: {delete_response.text}")
                continue
            print(f"Deleted Gist: {gist['id']}")

def main():
    parser = argparse.ArgumentParser(description='Upload Python files in a directory to Gist.')
    parser.add_argument('directory', type=str, nargs='?', help='the directory to upload')
    parser.add_argument('--ext', nargs='+', default=['.py'], help='file extensions to include')
    parser.add_argument('--prune', action='store_true', help='delete all gists created by this application')
    args = parser.parse_args()

    if args.directory:
        directory = args.directory
        description = os.path.basename(os.getcwd()) + " [code2gist]"
        files = get_files_in_directory(directory, args.ext)
        response = create_gist(description, files)
        if response:
            for filename, file_info in response['files'].items():
                print(f"\n- File: {filename}")
                print(f" URL: {file_info['raw_url']}")
                print()
    if args.prune:
        delete_old_gists()

if __name__ == "__main__":
    main()
