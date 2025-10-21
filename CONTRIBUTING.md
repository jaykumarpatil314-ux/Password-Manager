# Contributing to SecureVault Password Manager

Thank you for considering contributing to SecureVault! This document outlines the process for contributing to the project and how to report issues.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Styleguides](#styleguides)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Styleguide](#python-styleguide)
  - [JavaScript Styleguide](#javascript-styleguide)
  - [Documentation Styleguide](#documentation-styleguide)
- [Project Structure](#project-structure)

## Code of Conduct

This project and everyone participating in it is governed by the SecureVault Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers understand your report, reproduce the behavior, and find related reports.

**Before Submitting A Bug Report:**

- Check the [issues](https://github.com/jaykumarpatil314-ux/Password-Manager/issues) to see if the problem has already been reported
- Perform a cursory search to see if the problem has been reported already
- Determine which repository the problem should be reported in (frontend or backend)

**How Do I Submit A Good Bug Report?**

Bugs are tracked as GitHub issues. Create an issue and provide the following information:

- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples to demonstrate the steps
- Describe the behavior you observed after following the steps
- Explain which behavior you expected to see instead and why
- Include screenshots if possible
- Include details about your configuration and environment

### Suggesting Features

This section guides you through submitting an enhancement suggestion, including completely new features and minor improvements to existing functionality.

**Before Submitting An Enhancement Suggestion:**

- Check if the enhancement has already been suggested
- Determine which repository the enhancement should be suggested in

**How Do I Submit A Good Enhancement Suggestion?**

Enhancement suggestions are tracked as GitHub issues. Create an issue and provide the following information:

- Use a clear and descriptive title
- Provide a detailed description of the suggested enhancement
- Explain why this enhancement would be useful to most users
- List some other applications where this enhancement exists, if applicable
- Specify which version you're using
- Specify the name and version of the OS you're using

### Pull Requests

- Fill in the required template
- Do not include issue numbers in the PR title
- Include screenshots and animated GIFs in your pull request whenever possible
- Follow the [styleguides](#styleguides)
- Include thoughtfully-worded, well-structured tests
- Document new code
- End all files with a newline

## Development Setup

To set up the development environment:

1. Clone the repository:
   ```bash
   git clone https://github.com/jaykumarpatil314-ux/Password-Manager.git
   cd Password-Manager
   ```

2. Backend setup:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Frontend setup:
   ```bash
   cd frontend
   # Load as unpacked extension in Chrome
   ```

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Consider starting the commit message with an applicable emoji:
    * 🔒 `:lock:` when dealing with security
    * ✨ `:sparkles:` when adding a new feature
    * 🐛 `:bug:` when fixing a bug
    * 📝 `:memo:` when adding or updating documentation
    * 🧹 `:broom:` when refactoring code
    * 🧪 `:test_tube:` when adding tests

### Python Styleguide

* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Use docstrings for all public methods and classes
* Use type hints where appropriate
* Use meaningful variable names

### JavaScript Styleguide

* Use ES6+ features where appropriate
* Use camelCase for variable and function names
* Add JSDoc comments for all functions and classes
* Prefer const over let, and let over var
* Use meaningful variable names

### Documentation Styleguide

* Use [Markdown](https://daringfireball.net/projects/markdown/) for documentation
* Reference methods and classes in markdown using backticks: `Class.method()`
* Use code blocks with appropriate language syntax highlighting

## Project Structure

The project is divided into two main components:

- **Backend**: Flask-based API with database integration
- **Frontend**: Chrome extension with UI components

Please refer to the respective README files in each directory for more specific information about each component.

---

Thank you for contributing to SecureVault Password Manager!