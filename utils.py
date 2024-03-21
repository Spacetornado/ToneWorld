import pygame, sys, random, os, json, time
from settings import *

def get_player_image_name(file_path):
    # Extract just the filename without the path
    filename = os.path.basename(file_path)
    # Remove the file extension
    filename_without_extension = os.path.splitext(filename)[0]
    # Remove the "ch_" substring
    processed_filename = filename_without_extension.replace("ch_", "")
    return processed_filename

def are_coords_good(x, y):
    return not (x <= PLAYER_X_MIN or x >= PLAYER_X_MAX or y <= PLAYER_Y_MIN or y >= PLAYER_Y_MAX)

def read_json_with_retry(file_path, attempts=3, delay=0.1):
    """
    Reads a JSON file and returns its content. Retries up to 'attempts' times with a delay of 'delay' seconds between attempts in case of failure.
    """
    while attempts > 0:
        try:
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, 'r') as file:
                    return json.load(file)
            else:
                return []
        except Exception as e:
            logging.error(f"Error reading JSON file: {e}")
            time.sleep(delay)
            attempts -= 1
    return []

def write_json_with_retry(file_path, data, attempts=3, delay=0.1):
    """
    Writes data to a JSON file. Retries up to 'attempts' times with a delay of 'delay' seconds between attempts in case of failure.
    """
    while attempts > 0:
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            break
        except Exception as e:
            logging.error(f"Error writing JSON file: {e}")
            time.sleep(delay)
            attempts -= 1
