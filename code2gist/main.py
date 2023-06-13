import requests
import json
import os
import argparse

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
    return response.json()

def get_files_in_directory(directory):
    files = {}
    for root, dirnames, filenames in os.walk(directory):
        # Skip directories starting with .
        dirnames[:] = [d for d in dirnames if d[0] != '.']
        for filename in filenames:
            # Skip files starting with . and files not ending with .py
            if filename.startswith('.') or not filename.endswith('.py'):
                continue
            path = os.path.join(root, filename)
            rel_path = os.path.relpath(path, directory)  # get relative path
            with open(path, 'r') as file:
                try:
                    files[rel_path] = {"content": file.read()}  # use relative path as key
                except UnicodeDecodeError:
                    print(f"Could not read file: {path}")
    return files

def main():
    parser = argparse.ArgumentParser(description='Upload Python files in a directory to Gist.')
    parser.add_argument('directory', type=str, nargs='?', const=os.getcwd(), help='the directory to upload')
    args = parser.parse_args()
    directory = args.directory
    description = os.path.basename(directory)
    files = get_files_in_directory(directory)
    response = create_gist(description, files)
    for filename, file_info in response['files'].items():
        print(f"\n- File: {filename}")
        print(f" URL: {file_info['raw_url']}")

if __name__ == "__main__":
    main()
