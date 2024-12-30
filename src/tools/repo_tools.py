import requests
from src.tools.utils.repo import build_file_structure
from src.static.repo_static import repo_static

def get_repo_file_structure()->str:
    """
    This function gives file and folder structure of the repository.

    Args:
        None
    Returns:
        str: A nested dictionary representing the file structure in string format, 
             or an error message if the request fails or the response does not contain file paths.
    """

    # check if the file structure is already fetched
    if  repo_static.file_structure:
        return repo_static.file_structure

    # initialize the repo details
    repo_owner = repo_static.username
    repo_name = repo_static.repo
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/git/trees/main?recursive=1'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        data = response.json()

        # Ensure the response contains 'tree' and check if it has file paths
        if 'tree' in data:
            file_paths = [file['path'] for file in data['tree']]  # Extract file paths from the response
            file_structure = str(build_file_structure(file_paths))  # Build a nested dictionary from the file paths and return it as string representation
            repo_static.file_structure = file_structure
            return file_structure
        else:
            return "Error: No file paths found in the response data"
    except requests.exceptions.RequestException as e:
        # Handle the case where the API request fails
        return f"Error: Unable to fetch repository data. {str(e)}"

def explore_directory(path:str)->str:
    """
    This function will return the files
    and subdirectories at the specified path. If the path doesn't exist,
    it will suggest available options in the parent directory.

    Args:
        path (str): The path to explore.

    Returns:
        str: A string listing files and subdirectories, or suggestions if the path doesn't exist.
    """
    # initialize the repo details
    repo_owner = repo_static.username
    repo_name = repo_static.repo

    try:
        file_structure_str = get_repo_file_structure(repo_owner, repo_name)
        if isinstance(file_structure_str, str) and file_structure_str.startswith("Error"):
            return file_structure_str
        file_structure = eval(file_structure_str) # Safely evaluate the string representation of the dictionary

        # If root is provided
        if path == '/':
            return f"Files and Folders present at {path}:\n{'\n'.join(file_structure.keys())}"

        # Normalize the path
        path = path.strip('/').replace(' ', '/')
        parts = path.split('/')
        current_level = file_structure
        parent_path = ""

        # Traverse the file structure using the provided path
        for idx, part in enumerate(parts):
            if part in current_level:
                current_level = current_level[part]
                parent_path = "/".join(parts[:idx+1])
            else:
                # If the path doesn't exist, suggest available directories in the parent path
                return f"Path '{path}' not found.\nAvailable Files and folders in '{parent_path}':\n{'\n'.join(current_level.keys())}"

        # At the final level, return the list of files and directories
        return f"Files and Folders present at {path}:\n{'\n'.join(current_level.keys())}"
    except (SyntaxError, NameError, TypeError) as e:
        return f"Error processing file structure: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def get_file( file_path:str, branch:str='main')->str:
    """
    Given the file path, and branch, this function fetches the contents of the file
    from the raw GitHub URL.

    Args:
        file_path (str): The file path relative to the root of the repository (e.g., 'src/main/java/App.java').
        branch (str): The branch from which to fetch the file (default is 'main').

    Returns:
        str: The content of the file, or an error message if the file is not found or not supported.
    """
    # initialize the repo details
    repo_owner = repo_static.username
    repo_name = repo_static.repo

    # List of allowed file extensions for code-related files
    allowed_extensions = [
        '.py', '.java', '.js', '.html', '.css', '.cpp', '.c', '.h', '.json', '.xml', '.md', '.txt',
        '.rb', '.php', '.sh', '.bat', '.go', '.rs', '.swift', '.kt', '.ts', '.tsx', '.jsx', '.cs',
        '.vb', '.pl', '.pm', '.r', '.m', '.scala', '.sql', '.yaml', '.yml', '.ini', '.cfg', '.toml'
    ]

    # Check if the file extension is in the allowed list
    if not any(file_path.endswith(ext) for ext in allowed_extensions):
        return "Error: The file type is not supported for content retrieval.\nSupported file types: " + ", ".join(allowed_extensions)

    # Construct the raw GitHub URL
    url = f'https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{file_path}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.text  # Return the raw content of the file
    except requests.exceptions.RequestException as e:
        # Handle error case if the file is not found or there is any issue with the request
        return f"Error: Unable to fetch file content. {str(e)}.\nMake sure the file path is correct."

def save_summary(summary:str):
    """
    This function saves the summary of the repository.

    Args:
        summary (str): The summary of the repository.
    Returns:
        None
    """
    try:
        # Save the summary to the static object
        repo_static.summary = summary
        return "Summary saved successfully!"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
    
def get_repo_summary()->str:
    """
    This function gives the summary of the repository.

    Args:
        None
    Returns:
        str: The summary of the repository, or an error message if the request fails.
    """
    # check if the summary is already fetched
    if  repo_static.summary:
        return repo_static.summary
    else:
        return (
            "No summary found. It seems the repository summary has not been generated yet.\n"
            "delegate this task to the `repo_summarizer` agent to generate the summary.\n"
            "Once the summary is generated, I will save it and provide you with the result.\n"
        )