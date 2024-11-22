import os
import hashlib
from collections import defaultdict


def hash_file(filename, algorithm="md5"):
    """
    Computes the hash of a file.

    Args:
        filename (str): Path to the file to be hashed.
        algorithm (str): Hashing algorithm to use (default is 'md5').

    Returns:
        str: The hexadecimal hash of the file.
    """
    try:
        h = hashlib.new(algorithm)
        with open(filename, 'rb') as file:
            while chunk := file.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, ValueError) as e:
        print(f"Error hashing file {filename}: {e}")
        return None


def find_duplicates(folder, algorithm="md5"):
    """
    Finds duplicate files in a folder using file size as a preliminary filter.

    Args:
        folder (str): The root folder to search for duplicates.
        algorithm (str): Hashing algorithm to use (default is 'md5').

    Returns:
        dict: A dictionary mapping file hashes to lists of duplicate file paths.
    """
    size_map = defaultdict(list)
    duplicates = defaultdict(list)

    # Step 1: Group files by size
    for dirpath, _, filenames in os.walk(folder):
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            try:
                file_size = os.path.getsize(full_path)
                size_map[file_size].append(full_path)
            except OSError as e:
                print(f"Error accessing file {full_path}: {e}")

    # Step 2: Hash files within size groups
    for file_size, files in size_map.items():
        if len(files) > 1:  # Only process groups with potential duplicates
            hashes = {}
            for file in files:
                try:
                    file_hash = hash_file(file, algorithm)
                    if file_hash is None:
                        continue

                    # Check for duplicates
                    if file_hash in hashes:
                        duplicates[file_hash].extend([hashes[file_hash], file])
                    else:
                        hashes[file_hash] = file
                except Exception as e:
                    print(f"Error processing file {file}: {e}")

    return duplicates


def delete_duplicates(duplicates, interactive=True):
    """
    Deletes duplicate files.

    Args:
        duplicates (dict): A dictionary mapping file hashes to lists of duplicate file paths.
        interactive (bool): If True, prompt the user before deleting each duplicate. If False, delete automatically.
    """
    for file_hash, files in duplicates.items():
        # Keep only the first file, delete the rest
        original = files[0]
        duplicates_to_delete = files[1:]

        for duplicate in duplicates_to_delete:
            if interactive:
                response = input(f"Delete duplicate file: {duplicate}? (y/n): ").strip().lower()
                if response != 'y':
                    print(f"Skipped: {duplicate}")
                    continue

            try:
                os.remove(duplicate)
                print(f"Deleted: {duplicate}")
            except OSError as e:
                print(f"Error deleting file {duplicate}: {e}")


# Main logic
if __name__ == "__main__":
    folder_path = input("Enter the folder path to search for duplicates: ").strip()
    duplicates = find_duplicates(folder_path, algorithm="sha256")

    if duplicates:
        print("\nSummary of Duplicates:")
        for file_hash, files in duplicates.items():
            print(f"\nHash: {file_hash}")
            for file in files:
                print(f"  {file}")

        delete_option = input("\nDo you want to delete duplicates? (y/n): ").strip().lower()
        if delete_option == 'y':
            interactive = input("Enable interactive delete? (y/n): ").strip().lower() == 'y'
            delete_duplicates(duplicates, interactive=interactive)
        else:
            print("Duplicate files were not deleted.")
    else:
        print("No duplicates found.")
