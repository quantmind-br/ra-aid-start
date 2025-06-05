# RA Aid Start

A command-line interface (CLI) application for managing and executing command presets. This tool provides a menu-driven interface that allows users to save frequently used commands as presets and execute them easily.

## Features

- **Menu-driven interface**: Clean, visual terminal interface with Unicode box-drawing characters
- **Preset management**: Save, organize, and execute command presets
- **Persistent storage**: Presets are stored in a JSON file in your home directory
- **Easy navigation**: Intuitive menu system with numbered options
- **Command execution**: Execute saved commands directly from the interface

## Installation

### From source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ra-aid-start.git
cd ra-aid-start
```

2. Install in development mode:
```bash
pip install -e .
```

### Using pip (when published)

```bash
pip install ra-aid-start
```

## Usage

After installation, run the application using either:

```bash
ra-aid-start
```

or

```bash
python -m ra_aid_start
```

### Main Menu Options

1. **Select preset**: Choose and execute a saved command preset
2. **Configure presets**: Add new presets or delete existing ones
3. **Exit**: Close the application

### Managing Presets

#### Adding a new preset:
1. Select "Configure presets" from the main menu
2. Choose "Add new preset"
3. Enter a name for your preset
4. Enter the complete command to be executed

#### Deleting a preset:
1. Select "Configure presets" from the main menu
2. Choose "Delete existing preset"
3. Select the preset number to delete
4. Confirm the deletion

### Examples of useful presets

- `git status && git pull`: Check git status and pull latest changes
- `npm install && npm start`: Install dependencies and start development server
- `docker-compose up -d`: Start Docker containers in detached mode
- `pytest --verbose`: Run tests with verbose output

## Data Storage

Presets are stored in a JSON file located at:
```
~/.ra_aid_start_presets.json
```

This file is automatically created when you add your first preset.

## Requirements

- Python 3.6+
- No external dependencies (uses only Python standard library)

## Development

### Project Structure

```
ra_aid_start/
├── __main__.py          # Entry point
├── menus.py            # Menu display and user interaction logic
└── preset_manager.py   # Preset storage and management
```

### Building

```bash
python setup.py build
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.