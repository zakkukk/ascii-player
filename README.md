# ASCII Player

Transform videos into **colorful ASCII art** and play them in a window. Built with Python, OpenCV, and NumPy.

## Features

- Each video frame is converted into colored ASCII characters.
- Resizable playback window.
- Pause and resume using SPACE.
- Exit using Q, ESC, or the window's close button.
- The video automatically restarts when it reaches the end.
- Create a shareable `.exe` file without exposing the source code.

## Requirements

- Python 3.8 or higher.
- Dependencies listed in `requirements.txt`.

## Installation

```bash
git clone https://github.com/zakkukk/ascii-player.git
cd ascii-player
pip install -r requirements.txt
```

## Usage

Place a video named `video.mp4` inside the project folder and run:

```bash
python ascii_player.py
```

Alternatively, specify any video file:

```bash
python ascii_player.py path/to/my_video.mp4
```

| **Key** | **Action** |
|---|---|
| SPACE | Pause / Resume |
| Q or ESC | Exit |

## Configuration

At the top of `ascii_player.py`, you can customize the following variables:

| **Variable** | **Description** |
|---|---|
| `CARATTERI` | Characters used, from darkest to brightest. |
| `LARGHEZZA` | Characters per row (higher values provide more detail but reduce performance). |
| `LUMINOSITA` | Makes colors more or less vivid. |

**Tip:** The best results are achieved with videos featuring dark backgrounds and colorful subjects.

## Creating the Executable (Windows)

1. Place `video.mp4` inside the project folder.
2. Install PyInstaller:

   ```bash
   pip install pyinstaller
   ```

3. Build the executable:

   ```bash
   pyinstaller --onefile --noconsole --name ASCII-Player --add-data "video.mp4;." ascii_player.py
   ```

4. The executable will be available in:

   ```text
   dist/ASCII-Player.exe
   ```

### Notes

- The executable already includes the video, so you only need to share the `.exe` file.
- Your antivirus may flag the executable (this is relatively common with PyInstaller). You may need to verify the file before running it.
- If the application does not open, rebuild it without `--noconsole` to display error messages.

## Project Structure

```text
ascii-player/
├── ascii_player.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Video Disclaimer

The video is not included in this repository. Use your own videos or properly licensed content. Do not publish copyrighted material without permission.
