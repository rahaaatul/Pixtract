"""Main entry point for the video processing application."""

import os
import sys
import logging
from tqdm import tqdm
from colorama import Fore, Style, init
from typing import List, Any, Optional, Dict
import argparse

from .cli import parse_args
from .processing import process_video_frames
from . import config

init(autoreset=True)

def _configure_logging(verbose: bool) -> None:
    """Configures the logging for the application."""
    log_level: int = logging.DEBUG if verbose else logging.INFO
    log_format: str = config.LOG_FORMAT_VERBOSE if verbose else config.LOG_FORMAT_SIMPLE
    logging.basicConfig(level=log_level, format=log_format)

    if verbose:
        logging.debug(f"{Fore.CYAN}--- Verbose Mode Enabled ---")

def _validate_input_path(input_path: str) -> None:
    """Validates the existence and type of the input path."""
    if not os.path.exists(input_path):
        logging.error(f"Error: Input path '{input_path}' does not exist.")
        sys.exit(1)
    
    if not os.path.isfile(input_path) and not os.path.isdir(input_path):
        logging.error(f"Error: Input path '{input_path}' is neither a file nor a directory.")
        sys.exit(1)

def _determine_output_directory(input_path: str, output_directory_arg: Optional[str]) -> str:
    """Determines the output directory based on input path and provided argument."""
    if output_directory_arg is None:
        if os.path.isfile(input_path):
            output_directory_base = os.path.dirname(input_path)
            video_filename_no_ext = os.path.splitext(os.path.basename(input_path))[0]
            return os.path.join(output_directory_base, f"{video_filename_no_ext}{config.DEFAULT_SINGLE_VIDEO_OUTPUT_SUFFIX}")
        else: # is a directory
            return os.path.join(input_path, config.DEFAULT_DIRECTORY_OUTPUT_FOLDER)
    return output_directory_arg

def _prepare_output_directory(output_directory: str, dry_run: bool) -> None:
    """Checks if the output directory is writable and creates it if it doesn't exist."""
    if dry_run:
        return

    if os.path.exists(output_directory) and not os.access(output_directory, os.W_OK):
        logging.error(f"Error: Output directory '{output_directory}' is not writable.")
        sys.exit(1)
    elif not os.path.exists(output_directory):
        try:
            os.makedirs(output_directory)
            logging.debug(f"Created output directory: {output_directory}")
        except OSError as e:
            logging.error(f"Error creating output directory '{output_directory}': {e}", exc_info=True)
            sys.exit(1)

def _get_video_files(input_path: str, limit: Optional[int]) -> List[str]:
    """Discovers video files based on the input path and applies the limit."""
    if os.path.isfile(input_path):
        video_files: List[str] = [input_path]
    else: # is a directory
        video_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.lower().endswith(config.VIDEO_EXTENSIONS)]

    if limit:
        video_files = video_files[:limit]
    return video_files

import concurrent.futures

def _process_single_video(video_file: str, input_path: str, output_directory: str, processing_params: Dict[str, Any]) -> Dict[str, Any]:
    """Helper function to process a single video, used by the multiprocessing pool."""
    if os.path.isdir(input_path):
        video_specific_output_folder = os.path.join(output_directory, os.path.splitext(os.path.basename(video_file))[0])
    else:
        video_specific_output_folder = output_directory

    return process_video_frames(
        video_file,
        video_specific_output_folder,
        sharpness_threshold=processing_params["sharpness_threshold"],
        duplicate_threshold=processing_params["duplicate_threshold"],
        rotation_angle=processing_params["rotation_angle"],
        dry_run=processing_params["dry_run"],
        frame_interval=processing_params["frame_interval"]
    )

def _process_videos(video_files: List[str], input_path: str, output_directory: str, processing_params: Dict[str, Any], num_workers: int) -> List[Dict[str, Any]]:
    """Processes a list of video files in parallel and returns their processing summaries."""
    processing_summaries: List[Dict[str, Any]] = []
    
    # Use ProcessPoolExecutor for parallel processing
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Submit tasks to the executor
        future_to_video = {
            executor.submit(_process_single_video, video_file, input_path, output_directory, processing_params): video_file
            for video_file in video_files
        }

        # Use tqdm to show progress as futures complete
        with tqdm(total=len(video_files), desc="Processing Videos", unit="video", bar_format="{l_bar}{bar:20}{r_bar}") as pbar:
            for future in concurrent.futures.as_completed(future_to_video):
                video_file = future_to_video[future]
                try:
                    summary = future.result()
                    processing_summaries.append(summary)
                except Exception as exc:
                    logging.error(f'{video_file} generated an exception: {exc}', exc_info=True)
                    # Append a summary indicating failure for this video
                    processing_summaries.append({
                        "video": video_file,
                        "output_folder": "N/A",
                        "extracted_frames": 0,
                        "blurry_frames_removed": 0,
                        "duplicate_frames_removed": 0,
                        "final_frames_count": 0,
                        "status": "failed",
                        "error": str(exc)
                    })
                pbar.update(1)
    return processing_summaries

def _log_summaries(processing_summaries: List[Dict[str, Any]]) -> None:
    """Logs the individual and overall processing summaries."""
    total_frames_extracted: int = 0
    total_blurry_frames_removed: int = 0
    total_duplicate_frames_removed: int = 0
    total_final_frames_count: int = 0
    total_failed_videos: int = 0

    for summary in processing_summaries:
        if summary.get("status") == "failed":
            total_failed_videos += 1
            logging.error(f"\n{Fore.RED}Video: {summary['video']} - FAILED ({summary.get('error', 'Unknown error')})")
            continue

        total_frames_extracted += summary["extracted_frames"]
        total_blurry_frames_removed += summary["blurry_frames_removed"]
        total_duplicate_frames_removed += summary["duplicate_frames_removed"]
        total_final_frames_count += summary["final_frames_count"]

        logging.debug(f"\n{Fore.CYAN}Video: {summary['video']}")
        logging.debug(f"  {Fore.YELLOW}Output Folder: {summary['output_folder']}")
        logging.debug(f"  {Fore.BLUE}Extracted Frames: {summary['extracted_frames']}")
        logging.debug(f"  {Fore.RED}Blurry Frames Removed: {summary['blurry_frames_removed']}")
        logging.debug(f"  {Fore.MAGENTA}Duplicate Frames Removed: {summary['duplicate_frames_removed']}")
        logging.debug(f"  {Fore.GREEN}Final Frames Count: {summary['final_frames_count']}")

    logging.info(f"\n{Fore.GREEN}--- Overall Summary ---")
    logging.info(f"{Fore.BLUE}Total Extracted Frames: {total_frames_extracted}")
    logging.info(f"{Fore.RED}Total Blurry Frames Removed: {total_blurry_frames_removed}")
    logging.info(f"{Fore.MAGENTA}Total Duplicate Frames Removed: {total_duplicate_frames_removed}")
    logging.info(f"{Fore.GREEN}Total Final Frames Count: {total_final_frames_count}")
    if total_failed_videos > 0:
        logging.info(f"{Fore.RED}Total Videos Failed: {total_failed_videos}")

def main() -> None:
    """Main function to process all specified videos."""
    try:
        args, parser = parse_args()

        # If no arguments were provided, print help and exit
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(0)

        _configure_logging(args.verbose)

        input_path: str = args.input_path
        output_directory: Optional[str] = args.output
        sharpness_threshold: int = args.sharpness
        duplicate_threshold: float = args.duplicate_threshold
        rotation_angle: int = args.rotate
        dry_run: bool = args.dry_run
        limit: Optional[int] = args.limit
        frame_interval: int = args.interval
        num_workers: int = args.workers # New argument

        _validate_input_path(input_path)

        output_directory = _determine_output_directory(input_path, output_directory)
        
        video_files = _get_video_files(input_path, limit)
        _prepare_output_directory(output_directory, dry_run)

        processing_params = {
            "sharpness_threshold": sharpness_threshold,
            "duplicate_threshold": duplicate_threshold,
            "rotation_angle": rotation_angle,
            "dry_run": dry_run,
            "frame_interval": frame_interval
        }
        processing_summaries = _process_videos(video_files, input_path, output_directory, processing_params, num_workers) # Pass num_workers
        _log_summaries(processing_summaries)

    except KeyboardInterrupt:
        logging.info("\n\nProcessing interrupted by user. Exiting gracefully.")
        sys.exit(0)
    except SystemExit as e:
        if e.code != 0:
            # Error is already printed by argparse custom error handler
            pass
        sys.exit(e.code)
    except Exception as e:
        logging.error(f"An unhandled error occurred: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
