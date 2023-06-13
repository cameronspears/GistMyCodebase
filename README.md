## GistMyCodebase

This script automates the process of creating a private gist on GitHub that contains the codebase from the directory where the script is executed. It provides an easy and convenient way to privately share your codebases with language models like ChatGPT or other large language models (LLMs).

### Why Use GistMyCodebase?

- **Effortless Sharing**: Share your codebases with LLMs in a private and secure manner.
- **Condensed Code Copy**: Easily copy and paste the entire codebase within a single message or input prompt.
- **Better Collaboration**: Collaborate effectively by sharing codebases for review, debugging, or analysis.

### Usage

1. Make sure you have Python installed on your system.
2. Clone or download this repository to your local machine.
3. Open a terminal and navigate to the project directory.
4. Install the required dependencies: `pip install requests`.
5. Run the script: `python gistupload.py`.
6. The script will create a private gist with the codebase and display the URL of the gist in the terminal.

### Customization

You can customize the behavior of the script by modifying the following parameters:

- `YOUR_GITHUB_PERSONAL_ACCESS_TOKEN`: Replace this with your GitHub personal access token. Make sure it has the necessary permissions to create gists.
- Skipping files or directories: The script is configured to exclude hidden files and directories (those starting with `.`). You can modify the exclusion rules in the `get_files_in_directory` function to suit your needs.

### Limitations

- The GitHub Gist API has size limitations. Ensure that your codebase does not exceed the allowed size of 1GB per gist and individual files do not exceed 100MB.
- This script currently supports Python codebases only. Other languages or specific project structures may require modifications to the script.
