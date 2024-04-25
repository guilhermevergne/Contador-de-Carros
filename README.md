# Vehicle Detection and Tracking

This project utilizes a YOLOv5 model to detect and track vehicles in a video stream. It provides functionality to count vehicles and mark their positions as they move through the camera's field of view.

## Getting Started

These instructions will get your copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before running the project, make sure you have the following prerequisites installed on your system:
- Python (3.12.1 or newer)
- Chocolatey
- Makefile
- Pyenv

For WINDOWS users, open Windows Power-Shell as admin and run the following commands one by one:
```bash
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

choco install make

choco install pyenv-win
```
After the last command you may have to confirm typing 'y'

### Installing

To set up the project environment and install the necessary packages, run the following command:

```bash
make install
```

This will install all the required Python packages and set up the environment needed to run the vehicle detection and tracking program.

### Configuration

To configure the project settings, edit the params.txt file located in the ./src/app/ directory. The file should contain the following parameters:

- video_path: The path to the video file to be analyzed (default is './Assets/video.mp4').
- overlap_limit: The IoU threshold for vehicle tracking (default is 0.25).
- largura: The width of the video frame (default is 640).
- altura: The height of the video frame (default is 480).
- fps: The frames per second of the output video (default is 24).
- font_size: The font size of the vehicle count displayed (default is 72).
- padding: The padding around the vehicle count text (default is 10).

Ensure that your video file is placed in the path setted at 'params.txt'(default is 'video.mp4' in the folder 'Assets' at the root of the project directory).

### Runing the Program

To run the program, use the following command:

```bash
make run
```

This command will start the process of vehicle detection and tracking on the video specified in your params.txt configuration file. The output will be saved and can be reviewed after the program completes.