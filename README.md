# code2gist 📦

`code2gist` is a Python package that makes sharing your code projects easier than ever. With a simple command, it lets you upload your code files to GitHub's Gist. `code2gist` is available on [PyPI](https://pypi.org/project/code2gist/).

The package works hand-in-hand with OpenAI's ChatGPT-4's 'Browse with Bing' feature. Send codebases without going over the character limit using a secret URL. 🗜️

Another key feature of `code2gist` is its ability to handle a wide range of text-based file types, not just Python files. 📄

In addition, `code2gist` comes with a `prune` feature that provides a clean way to remove all the gists created by this tool from your GitHub account. 🌳

## Installation ⚙️

The recommended way to install `code2gist` is via `pipx`:

```
pipx install code2gist
```

`pipx` ensures the package and its dependencies are isolated from your global Python environment. Moreover, `pipx` automatically adds the installed package to your PATH, so you can run `code2gist` from any directory in the command line. 🧠

If you haven't installed `pipx` yet, you can do it by running `python3 -m pip install --user pipx` and then `python3 -m pipx ensurepath`.

You can still install the package via pip, but you will have to add the package directory to your PATH manually 😒:

```
pip install code2gist
```

### Adding code2gist Directory to the PATH Environment Variable 👣

Here are step-by-step instructions to add the code2gist directory to your PATH environment variable on Windows:

1. Open the **Control Panel**.
2. Navigate to **System and Security > System**.
3. Click on the **Advanced system settings** link on the left panel.
4. Click **Environment Variables**.
5. Under the **System Variables** section, find and double-click the variable **PATH**.
6. Click **New**.
7. Add the directory where code2gist is installed. For example, if you have Python 3.11 installed, the directory might look like this: `C:\...\Python311\Scripts`
8. Click **OK** to close all windows and save the changes.

After following these steps, your system should recognize code2gist commands from any directory in the command line. 👍

### GitHub Token 🔑

`code2gist` requires a GitHub token to function. You need to create a new token with the `gist` scope (which allows it to create gists). Follow [this guide](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) to create a new token.

Once you have your token, you should store it in the "GITHUB_TOKEN" environment variable. Here are the steps to set this variable in Windows:

1. Open the Control Panel.
2. Search for "Environment Variables".
3. Click on "Edit the system environment variables".
4. In the System Properties window that appears, click the "Environment Variables..." button.
5. In the Environment Variables window, click the "New..." button under the "User variables" section.
6. Enter "GITHUB_TOKEN" as the variable name and your token as the variable value.
7. Click "OK" on all open windows to apply the changes.

Please ensure that you have this variable set before using the package. ✅

## Usage 🚀

### Uploading Files 📤

To use `code2gist`, simply use the following command:

```
code2gist .
```

This command will upload all Python files in the current directory to a private Gist on your GitHub account. The Gist will be titled with the name of the current directory, followed by "[code2gist]".

If you want to include files with different extensions, you can specify them using the `--ext` option:

```
code2gist . --ext .txt .md .py
```

This command will include all text, Markdown, and Python files in the upload.

### Deleting Gists 🗑️

The `prune` feature allows you to delete all gists created by `code2gist`:

```
code2gist --prune
```

Running this command will delete all your gists with "[code2gist]" in the description.

## .gitignore and .code2gistignore Support ✅

`code2gist` respects `.gitignore` and `.code2gistignore` rules. Files that match a rule in either file will be skipped. 🦘

## Note 📝

The gists created by `code2gist` are private by default, providing a safe way for you to share your code without making it publicly available.

Please remember that `code2gist` is a tool for sharing code and should not be used to share sensitive information. Always ensure that your files do not contain any confidential data before uploading them.

## License ⚖️

`code2gist` is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

------

We hope `code2gist` serves as a valuable tool in your development toolkit. Happy coding! 💻👨‍💻
