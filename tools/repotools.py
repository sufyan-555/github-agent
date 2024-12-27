import requests
from tools.utils.repo import build_file_structure

repo_file_structure_cache = {}

def get_repo_file_structure(repo_owner:str, repo_name:str)->str:
    """
    This function makes a request to the GitHub API to retrieve the file structure of the specified repository.
    It constructs the API URL using the provided repository owner and name, and sends a GET request to this URL.
    If the request is successful and the response contains file paths, it builds a nested dictionary representing
    the file structure and returns it as a string. If the request fails or the response does not contain file paths,
    it returns an appropriate error message.

    Args:
        repo_owner (str): The owner of the repository (e.g., 'octocat').
        repo_name (str): The name of the repository (e.g., 'Hello-World').
    Returns:
        str: A nested dictionary representing the file structure in string format, 
             or an error message if the request fails or the response does not contain file paths.
    """
    repo_key = (repo_owner, repo_name)
    if repo_key in repo_file_structure_cache:
        return repo_file_structure_cache[repo_key]

    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/git/trees/main?recursive=1'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        data = response.json()

        # Ensure the response contains 'tree' and check if it has file paths
        if 'tree' in data:
            file_paths = [file['path'] for file in data['tree']]  # Extract file paths from the response
            file_structure = str(build_file_structure(file_paths))  # Build a nested dictionary from the file paths and return it as string representation
            repo_file_structure_cache[repo_key] = file_structure
            return file_structure
        else:
            return "Error: No file paths found in the response data"
    except requests.exceptions.RequestException as e:
        # Handle the case where the API request fails
        return f"Error: Unable to fetch repository data. {str(e)}"

def explore_directory(repo_owner:str, repo_name:str, path:str)->str:
    """
    Given a repository owner, name, and a path, this function will return the files
    and subdirectories at the specified path. If the path doesn't exist,
    it will suggest available options in the parent directory.

    Args:
        repo_owner (str): The owner of the repository.
        repo_name (str): The name of the repository.
        path (str): The path to explore.

    Returns:
        str: A string listing files and subdirectories, or suggestions if the path doesn't exist.
    """
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


def get_file(repo_owner:str, repo_name:str, file_path:str, branch:str='main')->str:
    """
    Given the repository owner, name, file path, and branch, this function fetches the contents of the file
    from the raw GitHub URL.

    Args:
        repo_owner (str): The owner of the repository (e.g., 'octocat').
        repo_name (str): The name of the repository (e.g., 'Hello-World').
        file_path (str): The file path relative to the root of the repository (e.g., 'src/main/java/App.java').
        branch (str): The branch from which to fetch the file (default is 'main').

    Returns:
        str: The content of the file, or an error message if the file is not found or not supported.
    """
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
