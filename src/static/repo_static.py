
class RepoStatic():
    def __init__(self):
        self.username = None
        self.repo = None
        self.file_structure = None
        self.summary = None

    def update_repo_details(self, username:str, repo:str):
        self.username = username
        self.repo = repo
        self.file_structure = None

    def add_file_structure(self, file_structure:dict):
        self.file_structure = file_structure

repo_static = RepoStatic()