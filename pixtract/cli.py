"""Command-line interface for the video processor."""

import argparse
import os
import sys
from . import config

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help(sys.stderr)
        self.stderr.write(f'\nerror: {message}\n')
        sys.exit(2)

def positive_int(value: str) -> int:
    """Type function for argparse to ensure a positive integer."""
    ivalue = int(value)
    if ivalue < 1:
        raise argparse.ArgumentTypeError("{value} is an invalid positive int value. Must be >= 1.")
    return ivalue

def parse_args() -> tuple[argparse.Namespace, argparse.ArgumentParser]:
    """
    Parses command-line arguments.

    Returns:
        tuple[argparse.Namespace, argparse.ArgumentParser]: A tuple containing the parsed arguments and the parser object.
    """
    parser = CustomArgumentParser(
        description="""Pixtract: A command-line tool to extract high-quality, non-blurry, and non-duplicate frames from videos.
        It helps in curating a collection of the best visual moments from your video footage.""",
        formatter_class=argparse.RawTextHelpFormatter # Use RawTextHelpFormatter for multiline descriptions
    )

    # Input/Output Options
    io_group = parser.add_argument_group("Input/Output Options")
    io_group.add_argument(
        "input_path",
        nargs='?',
        default=os.getcwd(),
        help="""Path to a video file or a directory containing videos.
If a directory is provided, all supported video files within it will be processed.
Defaults to the current working directory if not specified."""
    )
    io_group.add_argument(
        "-o", "--output",
        default=None,
        help="""Path to the output directory where extracted frames will be saved.
If not specified:
  - For a single video input: Frames are saved in a new folder next to the video (e.g., 'video_frames').
  - For a directory input: Frames are saved in a 'Processed_Frames' folder within the input directory."""
    )

    # Processing Parameters
    processing_group = parser.add_argument_group("Processing Parameters")
    processing_group.add_argument(
        "-i", "--interval",
        type=positive_int,
        default=config.DEFAULT_INTERVAL,
        help=f"Interval at which to extract frames. Default is {config.DEFAULT_INTERVAL} (every frame)."
    )
    processing_group.add_argument(
        "-s", "--sharpness",
        type=int,
        default=config.DEFAULT_SHARPNESS_THRESHOLD,
        help=f"""Set the sharpness threshold for blur detection.
Frames with sharpness values below this threshold will be considered blurry and discarded.
Lower values are more permissive (allow more blur). Default is {config.DEFAULT_SHARPNESS_THRESHOLD}."""
    )
    processing_group.add_argument(
        "-d", "--duplicate",
        type=float,
        dest="duplicate_threshold",
        metavar='THRESHOLD',
        default=config.DEFAULT_DUPLICATE_THRESHOLD,
        help=f"""Set the threshold for duplicate detection.
Higher values (closer to 1.0) are more strict, meaning frames must be nearly identical to be considered duplicates.
Lower values (closer to 0.0) are more permissive (allow more differences). Default is {config.DEFAULT_DUPLICATE_THRESHOLD}."""
    )
    processing_group.add_argument(
        "-r", "--rotate",
        type=int,
        choices=[0, 90, 180, 270],
        default=config.DEFAULT_ROTATION_ANGLE,
        help=f"Rotate extracted frames by 0, 90, 180, or 270 degrees. Default is {config.DEFAULT_ROTATION_ANGLE} (no rotation)."
    )

    # General Options
    general_group = parser.add_argument_group("General Options")
    general_group.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (debug) output, showing more detailed processing information."
    )
    general_group.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the process without actually creating or deleting any files. Useful for testing parameters."
    )
    general_group.add_argument(
        "-l", "--limit",
        type=int,
        default=None,
        help="Limit the number of videos to process when an input directory is provided."
    )
    general_group.add_argument(
        "-w", "--workers",
        type=positive_int,
        default=os.cpu_count(),
        help=f"Number of parallel processes to use for video processing. Default is {os.cpu_count()} (number of CPU cores)."
    )

    return parser.parse_args(), parser
