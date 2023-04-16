# Contributing to the django-upload-to project

Thank you for your interest in contributing to the django-upload-to project! Here are some guidelines to help you get started.

## How to Contribute

1. Check the list of [open issues](https://github.com/valbertovc/django-upload-to/issues) and choose one to work on or create a new feature proposal.
2. Fork the repository and create a branch with the name of your contribution.
3. Code your contribution, making meaningful commits and testing locally.
4. Ensure that your contribution meets the project's code standards, as well as Python code style requirements of [PEP 8](https://peps.python.org/pep-0008/).
5. Submit a pull request to the main branch of the repository.
6. Wait for community feedback and make any necessary changes.

## Development Environment

To set up a local development environment, follow the instructions below:

1. Fork the repository by clicking on the "Fork" button in the top right corner of this page.
2. Clone your forked repository to your local machine:
```bash
git clone https://github.com/<your-account>/django-upload-to.git
```
3. Install the [Poetry package manager](https://python-poetry.org/docs/#installation) by following the instructions in the official documentation.
4. Install the project dependencies using Poetry:
```bash
cd django-upload-to
poetry install
```
5. Run the tests:
```bash
python manage.py test
```

## Code Standards

The django-upload-to project follows the Python code style requirements of PEP 8. Please make sure to follow these standards when contributing to the project.

To ensure that your code meets the PEP 8 code standards, the project uses pre-commit. [Pre-commit](https://pre-commit.com/) is a tool that runs automated checks on your code before allowing you to make a commit. This helps to catch style issues before the code is reviewed.

To use pre-commit in the project, follow these steps:

1. Make sure you have pre-commit installed on your machine. If you don't have it installed already, install it using the command below:

```bash
pip install pre-commit
```

2. In the root of the project, run the following command to install the pre-commit hooks:

```bash
pre-commit install
```

3. Now, whenever you make a commit, pre-commit will automatically run the checks on your code.

```bash
pre-commit run
```

Please note that pre-commit checks can generate errors. If you encounter an error while making a commit, fix it before attempting to make the commit again.

## Commit Guidelines
We follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification for commit messages in this project. This helps us maintain a consistent commit history and makes it easier to generate changelogs.

The Conventional Commits specification defines a simple set of rules for creating commit messages:

* Each commit message must have a **type**, a **scope** (optional), and a **subject**.
* The type must be one of the following: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, or `chore`.
* The **scope** is optional and should be a short description of the affected component (e.g., `auth`, `views`, `models`).
* The **subject** is a brief description of the changes being made.
* In addition, please include the issue ID related to the commit in the message body, using the format `#<issue-id>`. 
* The subject line should be no longer than 72 characters.
Here is an example of a good commit message:

```text
feat(auth): add support for two-factor authentication

Refs #123
```

## Branch Naming Guidelines

We use a simple naming convention for branches:

* `feature/<branch-name>` for branches that add new features. Use letters in lowercase separated by hyphens to separate words. For example: `feature/add-file-uploads`.
* `bugfix/<branch-name>` for branches that fix bugs. Include the related issue ID in the name. For example: `bugfix/123-fix-login`.
* `hotfix/<branch-name>` for branches that fix critical issues in production.
* If you're working on a set of related changes, include a prefix that describes the set. For example: epic/user-profile-page or refactor/admin-pages.
When naming your branch, use a descriptive name that summarizes the changes you are making.

## Pull Requests

When submitting a pull request, please ensure that it meets the following guidelines:

* The changes are covered by tests.
* The commit messages follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.
* The pull request includes a clear description of the changes being made and steps to reproduce/check it.

## Issues and Suggestions

If you encounter any issues or have any suggestions for the project, please create an issue in the [issue tracker](https://github.com/valbertovc/django-upload-to/issues).

Thank you again for contributing to the django-upload-to project!