import os
import shutil


def organizer(folder, file_types=None):
    """
    Organizes files in the given folder into subfolders based on their extensions.

    Args:
        folder (str): Path to the folder to organize.
        file_types (dict, optional): Dictionary defining file categories and their extensions.
                                     Defaults to predefined categories.
    """
    # Default file categories if none are provided
    if file_types is None:
        file_types = {
            'Images': ['.jpeg', '.jpg', '.png', '.gif'],
            'Videos': ['.mp4', '.avi', '.mov'],
            'Documents': ['.pdf', '.docx', '.txt'],
            'Archives': ['.zip', '.rar']
        }

    # Create a fallback category for uncategorized files
    fallback_folder = os.path.join(folder, "Others")
    os.makedirs(fallback_folder, exist_ok=True)

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

        # Skip directories
        if not os.path.isfile(file_path):
            continue

        # Determine file extension
        ext = os.path.splitext(filename)[1].lower()

        # Find the target folder
        target_folder = fallback_folder
        for folder_name, extensions in file_types.items():
            if ext in extensions:
                target_folder = os.path.join(folder, folder_name)
                break

        # Create the target folder if it doesn't exist
        os.makedirs(target_folder, exist_ok=True)

        # Move the file, handling name conflicts
        try:
            target_path = os.path.join(target_folder, filename)
            if os.path.exists(target_path):
                # Add a numeric suffix to the file name to avoid overwriting
                base, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(target_path):
                    target_path = os.path.join(target_folder, f"{base}_{counter}{ext}")
                    counter += 1

            shutil.move(file_path, target_path)
            print(f"Moved {filename} to {os.path.basename(target_folder)}")
        except Exception as e:
            print(f"Error moving file {filename}: {e}")


# Example usage
organizer('/path/to/Downloads')
