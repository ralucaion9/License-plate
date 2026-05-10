# License Plate Recognition

A small Python project that detects license plates from a webcam feed and reads
the text on the plate using OCR.

## How it works

The app opens a small Tkinter window with two buttons:

- **Capture** opens the webcam, runs a Haar cascade classifier on each frame
  and draws a box around any detected plate. Press `s` to save the cropped
  plate, or `q` to quit.
- **Read** loads the last saved plate and runs easyocr on it to extract the
  text, then displays the result with matplotlib.

The cascade file (`haarcascade_russian_plate_number.xml`) is the standard one
shipped with OpenCV. It works best on plates with proportions similar to
Russian/European formats — accuracy drops for plates that look very different.

## Requirements

- Python 3.8+
- A webcam

Install the Python dependencies with:

```
pip install -r requirements.txt
```

`tkinter` ships with Python on Windows and macOS. On Debian/Ubuntu you may
need `sudo apt install python3-tk`.

## Running

```
python project1.py
```

Captured plates are written to a local `captures/` folder.

## Notes

- First run of `Read` will download the easyocr English model (a few hundred MB).
- Detection is sensitive to lighting and camera angle; tilt the camera so the
  plate is roughly horizontal for best results.
- This was a learning project for OpenCV and basic OCR, not a production tool.
