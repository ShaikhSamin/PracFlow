# PracFlow

> PracFlow — a command-line tool that creates standard practical assignment folders and starter files automatically.

**Team:** Samin , Anirudh
**Repository:** [URL]
**Date:** 28-10-2026

---

## 1. The problem

> Do not describe a problem in general terms. Describe **a thing you personally do**, repeatedly, that is slower than it should be.
>
> You must include evidence from your own machine. This is not optional.

### What we keep doing by hand

> Write the actual sequence of commands you run today, exactly as you type them.

'''bash
cd ~/Documents/Practical3
python3 utility.py
python3 practical4_recursion_exceptions.py
python3 practical6_oop_dunder.py
touch run.py
'''

### Evidence that this is real

> Prove you actually do this. Your shell remembers.

```bash
history | grep -E 'mkdir|touch' | wc -l
```

```
4

```

> I create or prepare practical assignment files several times while working on my MCA assignments. My shell history shows four matching mkdir or touch commands; I will measure the time saved after testing PracFlow.

### Who else has this problem

> My classmates may face a similar problem when creating folders and starter files for practical assignments. I will ask one classmate whether they repeat these steps and record their actual feedback.

---

## 2. Prior art — what already exists

> **This is the most important section in the document and the one that gets marked hardest.**
>
> The command line has been under continuous development since 1969. The chance that nobody has attempted your idea is close to zero. If you write "nothing like this exists", you have not looked.
>
> Your job is not to find an empty space. It is to find the *closest existing things* and say precisely where they stop being useful for your case.

### Tools we found and actually tried

| Copier 9.10.3 | PyPI / Copier documentation | Generates projects from templates; supports copying and updating projects | It is template-oriented; we need to test whether it conveniently creates our specific practical folders and starter files |

| Tool | Where we found it | What it does | Why it does not solve our problem |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

### Evidence of trying them

'''bash
~/Library/Python/3.9/bin/copier --version
copier 9.10.3
'''

```bash
~/Library/Python/3.9/bin/cookiecutter --version
```
Cookiecutter 2.6.0 from /Users/shaikhsamin/Library/Python/3.9/lib/python/site-packages (Python 3.9.6 ...)
```

Cookiecutter successfully reported its installed version as 2.6.0. During the project-generation test, it asked 11 configuration questions but failed during the post-generation hook with a "TypeError" related to an unsupported operation between "type" and "NoneType". Therefore, successful project generation could not be verified. This test showed that Cookiecutter can provide reusable project templates, but its generation process did not complete successfully in our test environment. We still need a tool that can quickly create our specific practical assignment folders and starter files with minimal manual effort.

### Where we searched


- [>] `man -k <keyword>` — searched the manual pages on our own machines
- [ ] GitHub search
- [ ] Homebrew: `brew search <keyword>`
- [ ] Stack Overflow — is somebody asking for this?
- [>] npm / PyPI
- [ ] Asked a human: [who, and what they said]

### The gap, in one sentence

> Existing tools can generate projects from reusable templates, but our workflow needs a simple command that creates the specific practical-assignment folders and starter files we repeatedly make by hand.

> **If you cannot complete that sentence, stop and talk to me before going further.** A project with no gap is not a failed project — it is a project that needs its scope adjusted, and that is a normal thing that happens to real engineers. Finding out now is cheap. Finding out in your presentation is not.

---

## 3. What we are building

### In scope

> - Create a practical folder using a name supplied by the user.
- Generate standard starter files inside the folder.
- List the files and folders created by the tool.
- Provide `--help` and `--dry-run` options.

### Out of scope

> - Automatically submit assignments to Google Classroom.
- Create or modify files outside the user-selected project directory.

### How we will know it worked

> This tool is successful if it turns several manual folder and file creation commands into one command, and we actually use it after the assignment ends.

---

## 4. Tech stack

| Choice | What we picked | Why, and what we rejected |
|---|---|---|
| Language | Python 3 | Easy to learn and suitable for creating folders and files. We rejected Bash because Python is easier to maintain as the project grows. |
| Argument parsing | `argparse` | Built into Python and supports `--help`, `--dry-run`, and other command-line options without installing extra packages. |
| Other dependencies | Python standard library only | Modules such as `pathlib` and `shutil` are enough for basic filesystem operations. |
| Testing | Python `unittest` | Built into Python and lets us test folder creation and error handling without extra dependencies. |
| Packaging / install method | Run using `python3 pracflow.py` | Simple for a student project; no package installation is required. |

---

## 5. Architecture

flowchart TD
    A[User runs PracFlow] --> B[Parse command-line arguments]
    B --> C{Valid arguments?}
    C -->|No| D[Show error and help]
    C -->|Yes| E{Dry run?}
    E -->|Yes| F[Show planned folders and files]
    E -->|No| G[Create practical folder]
    G --> H[Generate starter files]
    F --> I[Exit]
    H --> I
```

### Components

| Part | Responsibility | File |
|---|---|---|
| Command-line interface | Reads folder name and flags | `pracflow.py` |
| Argument parser | Validates input and handles help and dry-run | `pracflow.py` |
| Folder generator | Creates the folder and starter files | `pracflow.py` |
| Tests | Checks expected folder and file creation | `test_pracflow.py` |

### Data flow

The user enters a practical folder name and optional flags through the command line. PracFlow validates the input, then either displays the folders and starter files that would be created when "--dry-run" is used or creates the requested folder and files using Python's "pathlib" module. The result is displayed in the terminal, and no external API or database is required.

### What happens when things go wrong

If this happens| The tool does this
The user does not provide a folder name| Display an error message and usage instructions.
A folder with the same name already exists| Display a clear error and avoid overwriting existing files.
The program does not have permission to create files| Display an error message explaining that the operation failed.

---

## 6. Usage

> This is the contract between your tool and its user. Write it **before** you finish building, because designing the interface first usually changes the design.

### Synopsis

```
python3 pracflow.py [options] <folder_name>
```

### Commands and flags

| Flag | Long form | What it does | Default |
|---|---|---|---|
| `-h` | `--help` | Shows usage instructions and exits | Off |
| `-n` | `--dry-run` | Shows planned folders and files without creating them | Off |
| `-v` | `--verbose` | Displays detailed progress messages | Off |

> `--dry-run` is strongly recommended for any tool that deletes, moves or changes things. It is also the single easiest way to make your demo safe to run live in front of the class.

### Examples

Basic use

$ python3 pracflow.py Practical8

Expected output:

Success: Created folder 'Practical8'
Created: README.md
Created: main.py
Created: notes.txt

With a flag

$ python3 pracflow.py Practical5 --dry-run

Expected output:

Dry run: no files or folders were created.
Would create folder: Practical8
Would create files: README.md, main.py, notes.txt

When it fails

$ python3 pracflow.py --nonsense

Expected output:

usage: pracflow.py [-h] [-n] [-v] folder_name
pracflow.py: error: unrecognized arguments: --nonsense
```

### Exit codes

| Code | Meaning |
|---|---|
| 0 | Command completed successfully. |
| 1 | Folder or file creation failed. |
| 2 | Invalid command-line arguments. |

### Installation

git clone <your-repository-url>
cd <your-repository-folder>
python3 pracflow.py --help

---

## 7. References

- "Python "argparse" documentation" (https://docs.python.org/3/library/argparse.html) — Reference for designing command-line arguments and help messages.
- "Python "pathlib" documentation" (https://docs.python.org/3/library/pathlib.html) — Reference for working with directories and file paths.
- "Python "unittest" documentation" (https://docs.python.org/3/library/unittest.html) — Reference for writing tests.
- "Copier documentation" (https://copier.readthedocs.io/) — Examined an existing project-template generator and tested its version and help commands.
- "Cookiecutter documentation" (https://cookiecutter.readthedocs.io/) — Examined an existing project-template generator and tested its version and generation workflow.
- "Yeoman documentation" (https://yeoman.io/) — Examined an existing project scaffolding tool using its Angular generator.
