# SDK Setup

To play Seawars, you need to write a Python script that uses the `seamaster` library.

!!! important "Single File Submission"
    Your entire bot submission must be contained in a **single Python file**. This file will be copied and pasted directly into the code editor on the battle page.

## Local Development Setup
While the game provides an online editor, we highly recommend setting up a local development environment for a better coding experience (autocomplete, linting, etc.).

### Prerequisites
*   **Python 3.10+**: Ensure Python is installed on your system. You can verify this by running `python --version` or `python3 --version` in your terminal.

### Setting Up a Virtual Environment (VS Code)
Visual Studio Code (VS Code) is the recommended editor. Follow these steps to set up your environment:

1.  **Open your project folder** in VS Code.
2.  Open the Command Palette (`Ctrl+Shift+P` used or `Cmd+Shift+P` on Mac).
3.  Type **Python: Create Environment** and select it.
4.  Choose **Venv**.
5.  Select your Python 3.10+ interpreter.
6.  VS Code will create a `.venv` folder and automatically activate it for your terminal.

If you work from the command line, activate the environment manually:

```bash
source .venv/bin/activate
```

### Installing the Library
Once your environment is active, install the `seamaster` library using pip:

```bash
pip install seamaster
```

You are now ready to start coding! The library provides all the necessary classes and types for building your bot.

## Next Steps
Now that your environment is set up, verify your installation by writing your first bot.

[Writing Your Bot](writing_bots.md){ .md-button .md-button--primary }
