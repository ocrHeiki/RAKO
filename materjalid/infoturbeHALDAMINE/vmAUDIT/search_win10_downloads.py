import datetime
import re
import os

def parse_log_entry_time(entry_text):
    """
    Parses the 'Creation time' from a log entry text into a datetime object.
    Handles potential variations in microsecond precision and ensures UTC interpretation.
    """
    creation_time_match = re.search(r"Creation time\s*:\s*(?P<time_str>.* UTC)", entry_text)
    if creation_time_match:
        time_str = creation_time_match.group("time_str").strip()
        try:
            # Truncate microseconds to 6 digits if more are present, as datetime can only handle 6
            time_str = re.sub(r"(\.\d{6})\d+ UTC", r"\1 UTC", time_str)
            # If microseconds are not present, add them for consistent parsing
            if not '.' in time_str:
                time_str = time_str.replace(" UTC", ".000000 UTC")
            
            # Parse the datetime string
            dt_object_utc = datetime.datetime.strptime(time_str, "%b %d, %Y %H:%M:%S.%f UTC")
            return dt_object_utc
        except ValueError as e:
            # Fallback for slightly different formats or other parsing issues
            # print(f"Warning: Could not parse time string '{time_str}' with microseconds. Trying without. Error: {e}")
            try:
                # Try parsing without microseconds if the first attempt fails
                dt_object_utc = datetime.datetime.strptime(time_str.split(".")[0] + " UTC", "%b %d, %Y %H:%M:%S UTC")
                return dt_object_utc
            except ValueError as e_no_micro:
                # print(f"Warning: Could not parse time string '{time_str}' even without microseconds. Error: {e_no_micro}")
                pass
    return None

def search_win10_logs(log_file_path, target_datetime, target_filename_parts):
    found_entries = []
    current_entry_lines = []
    
    # Check if the log file exists
    if not os.path.exists(log_file_path):
        print(f"Error: Log file not found at {log_file_path}")
        return []

    print(f"Processing {log_file_path}...")
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.startswith("Event number"):
                if current_entry_lines:
                    entry_text = "".join(current_entry_lines)
                    entry_time = parse_log_entry_time(entry_text)
                    
                    if entry_time and entry_time <= target_datetime:
                        # Check for filename parts, case-insensitive
                        filename_found = all(part.lower() in entry_text.lower() for part in target_filename_parts)
                        if filename_found:
                            found_entries.append(entry_text)
                current_entry_lines = [line]
            else:
                current_entry_lines.append(line)
        
        # Process the last entry after the loop
        if current_entry_lines:
            entry_text = "".join(current_entry_lines)
            entry_time = parse_log_entry_time(entry_text)
            if entry_time and entry_time <= target_datetime:
                filename_found = all(part.lower() in entry_text.lower() for part in target_filename_parts)
                if filename_found:
                    found_entries.append(entry_text)
    
    return found_entries

if __name__ == "__main__":
    # Target information
    target_filename = "Ninite 7ZIP AnyDesk CDBurnerXP Chrome Discord Installer"
    target_filename_parts = target_filename.split(" ")
    target_datetime_str = "11/11/2025 1:32 PM"

    # Convert target_datetime_str to a datetime object
    # The format needs to match the input string: "Month/Day/Year Hour:Minute AM/PM"
    try:
        # Assuming the target time is local and logs are UTC, we need to convert target to UTC or compare intelligently
        # For simplicity, we'll treat target as naive and log times as naive for direct comparison
        # (assuming UTC for logs implies a fixed offset that doesn't affect comparison order relative to a fixed target)
        target_datetime = datetime.datetime.strptime(target_datetime_str, "%m/%d/%Y %I:%M %p")
    except ValueError as e:
        print(f"Error parsing target datetime '{target_datetime_str}': {e}")
        exit(1)

    # Log files to search
    log_files_to_check = ["win10_application.txt", "win10_security.txt"]

    print(f"Searching for '{target_filename}' (parts: {target_filename_parts}) before or at {target_datetime}...")

    all_found_results = {}
    for log_file in log_files_to_check:
        print(f"\n--- Searching in {log_file} ---")
        results = search_win10_logs(log_file, target_datetime, target_filename_parts)
        if results:
            all_found_results[log_file] = results
            for i, entry in enumerate(results):
                print(f"\nFound in {log_file} (Entry {i+1}):\n{entry}\n{'='*50}")
        else:
            print(f"No matching entries found in {log_file}.")

    if not all_found_results:
        print("No matching entries found across all specified log files.")
