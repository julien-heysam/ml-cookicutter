{{cookiecutter.project_name}}
==============================

[![Tests](https://github.com/your-username/your-project/actions/workflows/python-test.yml/badge.svg)](https://github.com/your-username/your-project/actions/workflows/python-test.yml) [![codecov](https://codecov.io/gh/your-username/your-project/graph/badge.svg)](https://codecov.io/gh/your-username/your-project)

**Project Description:**

{{cookiecutter.description}}

## Features

- **Feature 1:** Description of the first key feature
- **Feature 2:** Description of the second key feature
- **Feature 3:** Description of the third key feature
- Additional features that highlight your project's unique capabilities

## Command Line Interface (CLI)

The project provides a CLI for various tasks. To access the CLI, use the main command:

```bash
(venv) ➜ project-name --help

Usage: project-name [OPTIONS] COMMAND [ARGS]...

  Command Line Interface for various tasks.

Options:
  --help  Show this message and exit.

Commands:
  command1   Description of command1
  command2   Description of command2
  command3   Description of command3
```

## Setup

### Prerequisites
- Python 3.x
- pip
- virtualenv (recommended)

### Installation

Use the `Makefile` to set up your project:

```bash
# Create virtual environment
make create_environment

# Install development dependencies
make dev-install  # or pip install -e ."[dev]"

# Install pre-commit hooks
pre-commit install

# Setup initial configuration
make setup
```

### Running the Project

#### Basic Usage

```bash
make run_fastapi_uvicorn
```

#### Development Usage

1. Update the `.env` file with necessary configuration:

   ```env
   LOG_LVL=DEBUG
   ENV_STATE=LOCAL
   DEBUG=True
   ```

2. Create a Launch Configuration in VSCode (optional):

   Add the following to `.vscode/launch.json`:

   ```json
   {
       "version": "0.2.0",
       "configurations": [
           {
               "name": "Python Debugger",
               "type": "debugpy",
               "request": "launch",
               "module": "uvicorn",
               "args": [
                   "src.interface.app:app",
                   "--port",
                   "8001",
                   "--reload"
               ],
               "jinja": true
           }
       ]
   }
   ```

3. Debug:
   - Set breakpoints
   - Start the debugger
   - Inspect variables and step through code

## Environment Variables

Create a `.env` file:

```bash
cp .env.template .env
```

Fill in the required environment variables.

## Performance and Testing

### Latency Testing

Use Locust for server load testing:

```bash
locust -f tests/load_tests.py --host=https://your-domain.com
-> and open `http://0.0.0.0:8089/
```

### Running Tests

```bash
# Run all tests
make test

# Run specific test types
make test_unit
make test_integration
```

## Documentation

### Build Documentation

```bash
# Generate HTML documentation
make build_doc

# Open documentation
cd docs/_build/html
open index.html
```

## Makefile Commands

| **Command**                | **Description**                        | **Usage**                     |
|----------------------------|----------------------------------------|-------------------------------|
| **create_environment**     | Sets up a Python virtual environment   | `make create_environment`     |
| **dev-install**            | Installs development dependencies      | `make dev-install`            |
| **format**                 | Formats code using Black               | `make format`                 |
| **lint**                   | Formats and lints code                 | `make lint`                   |
| **clean**                  | Removes bytecode, caches, etc.         | `make clean`                  |
| **test**                   | Runs tests with coverage               | `make test`                   |
| **build_doc**              | Generates HTML documentation           | `make build_doc`              |
| **run**                    | Starts the application                 | `make run`                    |

## Database Schema
![Database Schema](reports/database_schema.png)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - your.email@example.com

Project Link: [https://github.com/your-username/your-project](https://github.com/your-username/your-project)
