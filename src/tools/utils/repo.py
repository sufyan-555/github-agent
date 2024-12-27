def build_file_structure(file_paths):
    """
    Given a list of file paths, this function builds a nested dictionary
    representing the file structure.

    :param file_paths: List of file paths (e.g., ['src/main/java/App.java', 'README.md']).
    :return: A nested dictionary representing the file structure.
    """
    file_structure = {}

    for path in file_paths:
        parts = path.split('/')  # Split the file path into directory components
        current_level = file_structure

        # Traverse through the parts, creating directories if needed
        for part in parts[:-1]:  # Loop through all except the last (file name)
            if part not in current_level:
                current_level[part] = {}  # Create a new directory if it doesn't exist
            current_level = current_level[part]  # Move down to the next directory level

        # Add the file to the directory (the last part is the file name)
        file_name = parts[-1]
        if file_name not in current_level:
            current_level[file_name] = {}  # Use an empty dictionary or any metadata if needed

    return file_structure