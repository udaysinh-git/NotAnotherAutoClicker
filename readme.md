# AutoClicker

AutoClicker is a simple and customizable auto-clicking application built using Python and PyQt5. It allows users to automate mouse clicks with adjustable click rates for both left and right mouse buttons.

## Features

- Adjustable click rates for left and right mouse buttons.
- Customizable hotkeys to start and stop clicking.
- Frameless and transparent window with a draggable title bar.
- Background animation using GIFs.

## Requirements

- Python 3.12 or higher
- PyQt5
- pynput

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/udaysinh-git/NotAnotherAutoClicker.git
   cd NotAnotherAutoClicker
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Program

1. Ensure the virtual environment is activated:
   ```sh
   .venv\Scripts\activate
   ```

2. Run the program:
   ```sh
   python main.py
   ```

## Building the Executable

1. Ensure the virtual environment is activated:
   ```sh
   .venv\Scripts\activate
   ```

2. Install PyInstaller:
   ```sh
   pip install pyinstaller
   ```

3. Build the executable:
   ```sh
   pyinstaller AutoClicker.spec
   ```

4. The executable will be created in the dist directory.

### Handling Antivirus Issues

If you encounter issues with your antivirus software flagging the executable as a potential threat, follow these steps:

1. Temporarily disable real-time protection in your antivirus software.
2. Run the PyInstaller command again to build the executable.
3. Once the executable is created, add an exception for the executable or the dist directory in your antivirus settings.
4. Re-enable real-time protection.

## Download the Release (if they exist)

You can download the latest release from the [Releases](https://github.com/udaysinh-git/NotAnotherAutoClicker/releases) page on GitHub.

## Usage

1. Open the AutoClicker executable.
2. Adjust the click rates for the left and right mouse buttons using the spin boxes.
3. Use the "Start Left" and "Start Right" buttons to start auto-clicking.
4. Use the hotkeys (default: `x2` for left and `x1` for right) to start and stop auto-clicking.

## License

This project is licensed under the MIT License. See the 

LICENSE

 file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or suggestions, please contact me.