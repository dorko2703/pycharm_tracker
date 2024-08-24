import os
import time
import subprocess
from datetime import datetime
import csv

# Define the name of the PyCharm process (may vary based on your PyCharm version)
PYCHARM_PROCESS_NAME = "pycharm"

# File to save the tracking information
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
tracking_file = os.path.join(desktop_path, "pycharm_time_tracking.csv")

# Initialize time tracking
start_time = None


def is_pycharm_active():
    """Check if PyCharm is the active window using xdotool."""
    try:
        active_window_id = subprocess.check_output(["xdotool", "getactivewindow"]).decode().strip()
        active_window_name = subprocess.check_output(
            ["xdotool", "getwindowname", active_window_id]).decode().strip().lower()
        return PYCHARM_PROCESS_NAME in active_window_name
    except Exception as e:
        print(f"Error checking active window: {e}")
        return False


def save_to_csv(start, end, duration):
    """Save the session details to a CSV file."""
    file_exists = os.path.isfile(tracking_file)
    with open(tracking_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write header if the file doesn't exist
            writer.writerow(["Start Time", "End Time", "Duration (minutes)"])
        writer.writerow(
            [start.strftime('%Y-%m-%d %H:%M:%S'), end.strftime('%Y-%m-%d %H:%M:%S'), f"{duration / 60:.2f}"])


def main():
    global start_time

    while True:
        if is_pycharm_active():
            if start_time is None:
                start_time = time.time()
        else:
            if start_time is not None:
                end_time = time.time()
                duration = end_time - start_time
                save_to_csv(datetime.fromtimestamp(start_time), datetime.fromtimestamp(end_time), duration)
                start_time = None

        time.sleep(5)  # Check every 5 seconds


if __name__ == "__main__":
    print(f"Tracking time spent in PyCharm. Results will be saved to {tracking_file}.")
    try:
        main()
    except KeyboardInterrupt:
        print("Time tracking stopped by user.")
        if start_time is not None:
            end_time = time.time()
            duration = end_time - start_time
            save_to_csv(datetime.fromtimestamp(start_time), datetime.fromtimestamp(end_time), duration)
