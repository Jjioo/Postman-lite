# HTTP Request CLI

This is a command-line application built with Python that allows you to send HTTP requests (GET, POST, PUT, DELETE, PATCH, OPTIONS) to a specified URL. It provides a user-friendly interface with auto-completion and the ability to add headers and JSON request bodies.

## Features

- Send HTTP requests (GET, POST, PUT, DELETE, PATCH, OPTIONS) to a specified URL
- Auto-completion for URLs and methods
- Add custom headers to requests
- Include JSON request bodies from files
- Formatted JSON response display

## Requirements

- Python 3.x
- Required Python libraries (see `requirements.txt`)

## Installation

1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Install the required libraries by running: `pip install -r requirements.txt`

## Usage

1. Run the script by executing: `python main.py`
2. Select the desired HTTP method from the menu using the arrow keys and press Enter.
3. Enter the URL with optional flags:
   - `-h`: Add custom headers (enter key:value pairs, type 'done' when finished)
   - `-b`: Include a JSON request body from a file in the `Body` directory
4. The script will send the request and display the formatted response.
5. You will be prompted to try again or exit the application.

## Potential Errors

- **Invalid JSON file format**: Ensure that the JSON files in the `Body` directory are valid and well-formatted.
- **Error opening file**: This error may occur if the script is unable to open a file in the default editor. In this case, you will need to open the file manually using the provided file path.
- **Request failed**: This error may occur due to network issues or an invalid URL. Check your internet connection and ensure that the URL is correct.

## Supported Operating Systems

This application should work on Windows, macOS, and Linux operating systems. However, the way files are opened in the default editor may vary depending on the operating system.

- **Windows**: Files are opened using Notepad.
- **macOS and Linux**: Files are opened using the default editor associated with the `xdg-open` command.

If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.