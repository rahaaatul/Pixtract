# Pixtract 🎬

Pixtract is a powerful and intelligent command-line tool designed to extract high-quality, non-blurry, and non-duplicate frames from your videos. Whether you're building a computer vision dataset, analyzing video content, or simply curating the best visual moments, Pixtract streamlines the process, saving you time and disk space.

## ✨ Features

*   **Intelligent Frame Filtering:** 🧠 Automatically analyzes and discards blurry frames and efficiently removes duplicate or near-duplicate images, ensuring you only get sharp, unique, and relevant visuals.
*   **High-Performance Parallel Processing:** ⚡️ Leverages multiple CPU cores to process videos concurrently, significantly reducing processing times for large collections.
*   **Granular Frame Extraction Control:** 🎯 Extract frames at a specified interval (e.g., every 5th frame), giving you precise control over the density of your output.
*   **Wide Video Format Support:** 🎥 Extracts frames from a variety of popular video formats, including MP4, MOV, AVI, and MKV.
*   **Image Rotation:** 🔄 Corrects the orientation of frames with adjustable rotation (0, 90, 180, or 270 degrees).
*   **Batch Processing:** 📦 Process multiple videos from a given directory in a single run.
*   **Robust Error Handling:** ✅ Implemented robust error handling for individual video processing, ensuring the application continues even if some videos fail.
*   **Dry Run Mode:** 🧪 Simulate the entire process without creating or deleting any files, perfect for testing parameters.
*   **Verbose Output:** 📊 Get detailed logging information for debugging or deeper insights into the processing.

## ⬇️ Installation

You can install Pixtract directly from GitHub using `Git`:

```bash
pip install git+https://github.com/rahaaatul/Pixtract.git
```

Or from PyPI using `pip`:

```bash
pip install pixtract
```

For an isolated installation, use `pipx`:

```bash
pipx install pixtract
```

## 🚀 Usage

To use Pixtract, simply run the `pixtract` command with the path to your video file or a directory containing videos.

### Quick Start

Process a single video and save frames to a default output folder (e.g., `video_frames` next to your video):

```bash
pixtract "path/to/your/video.mp4"
```

Process all videos in a directory and save frames to a specified output folder:

```bash
pixtract "path/to/your/videos_directory" -o "path/to/your/output_folder"
```

### Examples

Extract frames from `my_movie.mp4`, remove blurry frames (sharpness threshold 50), and remove duplicates (threshold 0.98):

```bash
pixtract my_movie.mp4 -s 50 -d 0.98
```

Process videos in `my_videos/`, rotate frames by 90 degrees, and enable verbose output:

```bash
pixtract my_videos/ -r 90 -v
```

Extract every 10th frame from `my_video.mp4`:

```bash
pixtract my_video.mp4 -i 10
```

Simulate processing `holiday_clip.mp4` without actually saving or deleting files:

```bash
pixtract holiday_clip.mp4 --dry-run
```

## ⚙️ Command-Line Options

| Option              | Short | Type    | Default        | Description                                                                                             |
| :------------------ | :---- | :------ | :------------- | :------------------------------------------------------------------------------------------------------ |
| `--input-path`      |       | `str`   | Current Dir    | Path to a video file or a directory containing videos. If a directory, all supported video files within it will be processed. Defaults to the current working directory. |
| `--output`          | `-o`  | `str`   | `Processed_Frames` | Path to the output directory where extracted frames will be saved. Defaults vary based on input type.    |
| `--interval`        | `-i`  | `int`   | `1`            | Interval at which to extract frames (e.g., `5` for every 5th frame).                                    |
| `--sharpness`       | `-s`  | `int`   | `100`          | Set the sharpness threshold for blur detection. Lower values are more permissive (allow more blur).     |
| `--duplicate`       | `-d`  | `float` | `1.0`          | Set the threshold for duplicate detection. Higher values (closer to `1.0`) are more strict.             |
| `--rotate`          | `-r`  | `int`   | `0`            | Rotate frames by 0, 90, 180, or 270 degrees.                                                            |
| `--dry-run`         |       | `flag`  | `False`        | Simulate the process without creating or deleting files.                                                |
| `--limit`           | `-l`  | `int`   | `None`         | Limit the number of videos to process when an input directory is provided.                              |
| `--verbose`         | `-v`  | `flag`  | `False`        | Enable verbose (debug) output, showing more detailed processing information.                            |
| `--workers`         | `-w`  | `int`   | `CPU Cores`    | Number of parallel processes to use for video processing. Defaults to the number of CPU cores available. |

## 🧑‍💻 Development

To set up the project for development, clone the repository and install the development dependencies:

```bash
git clone https://github.com/rahaaatul/pixtract.git
cd pixtract
pip install -e .[dev]
```

### Running Tests

To run the test suite, ensure you have installed the development dependencies and then execute `pytest`:

```bash
pip install -e .[dev]
pytest
```

## 🤝 Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request. For bug reports, please use the [Bug Report template](https://github.com/rahaaatul/pixtract/issues/new?assignees=&labels=bug&projects=&template=bug_report.md&title=). For new features, use the [Feature Request template](https://github.com/rahaaatul/pixtract/issues/new?assignees=&labels=enhancement&projects=&template=feature_request.md&title=).

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.