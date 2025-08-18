# Pixtract v0.1.0 - Initial Release

In this initial release of Pixtract, we focused on providing a robust and efficient command-line tool for extracting high-quality, non-blurry, and non-duplicate frames from videos. This version introduces core functionalities for intelligent frame processing, parallel execution, and user-friendly controls.

## Highlights

*   **Intelligent Frame Filtering:** Automatically discards blurry and duplicate frames, ensuring only sharp, unique images are extracted.
*   **High-Performance Parallel Processing:** Leverages multiple CPU cores to process videos concurrently, drastically speeding up batch operations.
*   **Granular Frame Extraction Control:** Offers precise control over which frames are extracted, allowing users to specify an interval (e.g., every 5th frame).
*   **Robust Error Handling:** Ensures continuous operation even if individual video processing encounters issues, logging errors and proceeding with other tasks.
*   **Comprehensive Command-Line Interface:** Provides a rich set of options for input/output management, processing parameters, and debugging.

## Features

### Intelligent Frame Filtering

*   **Blur Detection (`-s`, `--sharpness`):** Implements a sophisticated blur detection algorithm that analyzes the sharpness of each frame using the Laplacian variance method. Frames falling below a user-defined sharpness threshold are automatically discarded, guaranteeing that only clear and focused images are retained. This is crucial for applications requiring high-quality visual data, such as machine learning datasets.
*   **Duplicate Frame Removal (`-d`, `--duplicate`):** Utilizes Structural Similarity Index (SSIM) to compare frames and identify near-duplicates. A configurable threshold allows users to define the level of similarity considered a duplicate. This feature significantly reduces redundant data, saving storage space and improving the efficiency of subsequent analyses.

### High-Performance Parallel Processing

*   **Concurrent Video Processing (`-w`, `--workers`):** The core processing logic has been refactored to utilize `concurrent.futures.ProcessPoolExecutor`. This enables Pixtract to process multiple video files simultaneously across available CPU cores, leading to a significant reduction in overall processing time, especially beneficial for large video collections. Users can specify the number of worker processes, or let the tool intelligently default to the system's CPU count.

### Granular Frame Extraction Control

*   **Frame Interval Extraction (`-i`, `--interval`):** Introduces a new command-line option that allows users to specify an interval for frame extraction. Instead of processing every single frame, users can now extract frames at a defined frequency (e.g., `-i 10` to extract every 10th frame). This feature provides fine-grained control over the output density, making it ideal for scenarios where a representative subset of frames is sufficient, thereby reducing processing time and output size.

### Robust Error Handling

*   **Individual Video Error Isolation:** The parallel processing pipeline is designed with robust error handling mechanisms. If an error occurs during the processing of a single video, the application logs the specific error for that video and gracefully continues with the remaining videos in the queue. This prevents a single problematic file from halting the entire batch process.
*   **Detailed Summary Reporting:** The final processing summary now includes a clear count of any videos that failed during processing, providing users with a comprehensive overview of the operation's success and any encountered issues.

### Comprehensive Command-Line Interface

*   **Flexible Input/Output (`--input-path`, `-o`, `--output`):** Supports processing of single video files or entire directories containing multiple videos. Output frames can be directed to a specified folder, with intelligent default naming conventions for single video and directory inputs.
*   **Image Rotation (`-r`, `--rotate`):** Allows for automatic rotation of extracted frames by 0, 90, 180, or 270 degrees, ensuring correct orientation regardless of the source video's metadata.
*   **Simulation Mode (`--dry-run`):** Provides a dry run option to simulate the entire processing workflow without actually creating or deleting any files. This is invaluable for testing parameters and verifying expected outcomes before committing to a full processing run.
*   **Verbose Output (`-v`, `--verbose`):** Enables a verbose logging mode that provides detailed, step-by-step information about the processing, including frame-by-frame analysis, file operations, and debugging insights.
*   **Processing Limit (`-l`, `--limit`):** When processing a directory, users can set a limit on the number of videos to be processed, useful for testing or partial batch operations.