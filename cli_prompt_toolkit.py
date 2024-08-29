import os
import json
import requests
import subprocess
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.keys import Keys
from prompt_toolkit.application import Application
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from colorama import init, Fore, Style as ColoramaStyle

init(autoreset=True)  # Initialize colorama


# File to store URLs
URL_FILE = "urls.txt"
BODY_DIR = "Body"  # Directory for JSON body files

def load_urls():
    if os.path.exists(URL_FILE):
        with open(URL_FILE, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    return []


import os
import subprocess

def open_file_in_editor(file_path):
    """Open a file in Notepad on Windows, or the default editor on other systems."""
    try:
        if os.name == 'nt':  # For Windows
            notepad = r"C:\Windows\System32\notepad.exe"
            subprocess.Popen([notepad, file_path])
        elif os.name == 'posix':  # For macOS and Linux
            subprocess.call(['xdg-open', file_path])
    except Exception as e:
        print(f"Error opening file: {e}")
        print("Please open the file manually: " + file_path)

def format_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Formatted JSON file: {file_path}")
    except Exception as e:
        print(f"Error formatting JSON file: {e}")
        
        
def save_url(url, saved_urls, url_completer):
    if url not in saved_urls:
        saved_urls.append(url)
        with open(URL_FILE, 'a') as f:
            f.write(f"{url}\n")
        url_completer.words.append(url)  # Update the completer
def format_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Formatted JSON file: {file_path}")
    except Exception as e:
        print(f"Error formatting JSON file: {e}")
        
def list_body_files():
    if os.path.exists(BODY_DIR):
        return [f for f in os.listdir(BODY_DIR) if f.endswith('.json')]
    return []

def create_method_selector(methods):
    class MethodSelector:
        def __init__(self):
            self.methods = methods
            self.selected_index = 0

        def get_formatted_methods(self):
            return [
                ("class:method" if i != self.selected_index else "class:selected_method",
                 f"{' → ' if i == self.selected_index else '   '}{method}")
                for i, method in enumerate(self.methods)
            ]

        def move_cursor(self, offset):
            self.selected_index = (self.selected_index + offset) % len(self.methods)

    selector = MethodSelector()
    methods_window = Window(
        FormattedTextControl(lambda: selector.get_formatted_methods()),
        height=len(methods) + 2,
    )

    app = Application(
        layout=Layout(HSplit([
            Window(height=1, char='-'),
            Window(FormattedTextControl("Select a method:"), height=1),
            Window(height=1, char='-'),
            methods_window,
            Window(height=1, char='-'),
        ])),
        key_bindings=get_key_bindings(selector),
        style=Style([
            ('method', '#ffffff'),
            ('selected_method', '#00ffff bold'),
        ]),
        full_screen=True,
    )

    return app, selector

def get_key_bindings(selector):
    from prompt_toolkit.key_binding import KeyBindings
    kb = KeyBindings()

    @kb.add(Keys.Left)
    def up(event):
        selector.move_cursor(-1)

    @kb.add(Keys.Right)
    def down(event):
        selector.move_cursor(1)

    @kb.add(Keys.Enter)
    def enter(event):
        event.app.exit()

    return kb



def get_file_key_bindings(selector, files):
    from prompt_toolkit.key_binding import KeyBindings
    kb = KeyBindings()

    @kb.add(Keys.Up)
    def up(event):
        selector.move_cursor(-1)

    @kb.add(Keys.Down)
    def down(event):
        selector.move_cursor(1)

    @kb.add(Keys.Right)
    def edit(event):
        file_path = os.path.join(BODY_DIR, files[selector.selected_index])
        open_file_in_editor(file_path)
        format_json_file(file_path)
        event.app.exit(result='edited')

    @kb.add(Keys.Enter)
    def enter(event):
        event.app.exit(result='selected')

    return kb

def select_body_file():
    files = list_body_files()
    if not files:
        print(Fore.RED + "No JSON files found in the Body directory.")
        return None

    class FileSelector:
        def __init__(self):
            self.files = files
            self.selected_index = 0

        def get_formatted_files(self):
            return [
                ("class:file" if i != self.selected_index else "class:selected_file",
                 f"{' → ' if i == self.selected_index else '   '}{file}\n")
                for i, file in enumerate(self.files)
            ]

        def move_cursor(self, offset):
            self.selected_index = (self.selected_index + offset) % len(self.files)

    selector = FileSelector()
    
    def get_file_key_bindings(selector):
        kb = KeyBindings()

        @kb.add(Keys.Up)
        def up(event):
            selector.move_cursor(-1)

        @kb.add(Keys.Down)
        def down(event):
            selector.move_cursor(1)

        @kb.add(Keys.Right)
        def edit(event):
            file_path = os.path.join(BODY_DIR, files[selector.selected_index])
            open_file_in_editor(file_path)
            format_json_file(file_path)
            event.app.exit(result='edited')

        @kb.add(Keys.Enter)
        def enter(event):
            event.app.exit(result='selected')

        return kb

    while True:
        files_window = Window(
            FormattedTextControl(lambda: selector.get_formatted_files()),
            height=len(files) + 2,
        )

        instruction_text = HTML("Select a JSON file: (Use arrow keys, <b><ansileft>Right Arrow</ansileft></b> to edit, <b><ansigreen>Enter</ansigreen></b> to select)")

        app = Application(
            layout=Layout(HSplit([
                Window(height=1, char='-'),
                Window(FormattedTextControl(instruction_text), height=1),
                Window(height=1, char='-'),
                files_window,
                Window(height=1, char='-'),
            ])),
            key_bindings=get_file_key_bindings(selector),
            style=Style([
                ('file', '#ffffff'),
                ('selected_file', '#00ffff bold'),
            ]),
            full_screen=True,
        )

        result = app.run()
        if result == 'selected':
            return files[selector.selected_index]
        elif result == 'edited':
            files = list_body_files()  # Refresh the file list
            selector.files = files
            selector.selected_index = min(selector.selected_index, len(files) - 1)
    
def main():
    session = requests.Session()
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']
    
    # Load saved URLs
    saved_urls = load_urls()
    
    # Create a PromptSession
    history = InMemoryHistory()
    url_completer = WordCompleter(saved_urls, ignore_case=True)
    method_completer = WordCompleter(methods + ['-h', '-b'], ignore_case=True)
    
    style = Style.from_dict({
        'highlight': '#00ff00 bold',
    })

    prompt_session = PromptSession(style=style, history=history)

    while True:
        try:
            # Display method menu and select method
            print("\033c", end='')  # Clear the console
            app, selector = create_method_selector(methods)
            app.run()
            selected_method = methods[selector.selected_index]
            print(f"{Fore.GREEN}Selected method: {Fore.YELLOW}{selected_method}")
            print()

            # Prompt user for URL and flags
            user_input = prompt_session.prompt(HTML("<ansicyan>Enter URL with optional flags (e.g., http://localhost:3000 -h -b): </ansicyan>"), completer=url_completer)

            if not user_input:
                print(f"{Fore.RED}No input received.")
                continue

            # Initialize headers and body
            headers = {}
            body = None

            # Parse URL and flags
            parts = user_input.split()
            url = parts[0]
            flags = parts[1:] if len(parts) > 1 else []

            # Save the URL and update the completer
            save_url(url, saved_urls, url_completer)

            # Handle headers
            if '-h' in flags:
                print(Fore.CYAN + "Enter headers (key:value). Type 'done' when finished:")
                while True:
                    header_input = prompt_session.prompt(HTML("<ansiyellow>Header: </ansiyellow>"))
                    if header_input.lower() == 'done':
                        break
                    try:
                        key, value = header_input.split(":", 1)
                        headers[key.strip()] = value.strip()
                    except ValueError:
                        print(f"{Fore.RED}Invalid header format. Use key:value format.")
                print()

            # Handle body
            if '-b' in flags:
                selected_file = select_body_file()
                if selected_file:
                    with open(os.path.join(BODY_DIR, selected_file), 'r') as f:
                        try:
                            body = json.load(f)
                        except json.JSONDecodeError:
                            print(f"{Fore.RED}Invalid JSON file format.")
                            continue
                    print()

            # Send the request
            try:
                if selected_method == "GET":
                    response = session.get(url, headers=headers)
                elif selected_method == "POST":
                    response = session.post(url, json=body, headers=headers)
                elif selected_method == "PUT":
                    response = session.put(url, json=body, headers=headers)
                elif selected_method == "DELETE":
                    response = session.delete(url, headers=headers)
                elif selected_method == "PATCH":
                    response = session.patch(url, json=body, headers=headers)
                elif selected_method == "OPTIONS":
                    response = session.options(url, headers=headers)

                # Pretty-print JSON response
                try:
                    response_json = response.json()
                    formatted_response = json.dumps(response_json, indent=4)
                except json.JSONDecodeError:
                    formatted_response = response.text
                
                print(Fore.CYAN + ColoramaStyle.BRIGHT + f"Response [{response.status_code}]:")
                print(Fore.GREEN + formatted_response)
                print()
            except requests.exceptions.RequestException as e:
                print(f"{Fore.RED}Request failed: {e}")

            # Ask if the user wants to try again
            try_again = prompt_session.prompt(HTML("<ansicyan>Do you want to try again? (y/n): </ansicyan>")).strip().lower()
            if try_again != 'y':
                break

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Operation cancelled.")
            break

if __name__ == "__main__":
    main()
