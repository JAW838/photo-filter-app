# photo-filter-app

Many technologically illiterate people have stockpiles of old photos that they want to sort
through. They want to go through them one by one, saving or discarding them.
<p>
This application is for those people. It provides a simple interface for presenting images
and marking them as important, unimportant, or permanently deleting them, before moving to the
next and starting over.

## Running The Project
Below are two ways to run the project: those who want to develop and those who just want to 
use the software

### Run to Use
From this page, find Releases. Click on it to open it and download the latest release as a .zip
file. Then go to the Downloads folder on your computer and find `photo-filter-app.zip`, right
click it and choose one of the extraction options. Then find the `photo-filter-app` folder and
enter it. Enter `dist` and run the `.exe` to run the program. It will prompt you to select a 
folder to sort. This folder should contain the images you want to sort. Select the folder and
the program will start.

### Run to Develop
The project can be run with `python -m app.main.App` and compiled with 
`python -m PyInstaller --noconsole --onefile -n PhotoSorter app/main/App.py`. To compile for 
debugging exclude `--noconsole`.

## In-depth Documentation

This application adheres to a simple two-tier architecture, a UI layer and a logic layer.

## Contributing

Contributions are welcome for expanding and maintaining the application.
