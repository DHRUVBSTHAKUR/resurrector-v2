import os
import shutil
from git import Repo
from github import Github, Auth
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

class GitManager:
    def __init__(self, workspace_path="./agent_workspace"):
        self.workspace_path = workspace_path
        self.current_repo = None
        
        if GITHUB_TOKEN:
            auth = Auth.Token(GITHUB_TOKEN)
            self.github_client = Github(auth=auth)
        else:
            print("⚠️ WARNING: GITHUB_TOKEN not found.")
        
        self._clear_workspace()

    def _clear_workspace(self):
        if os.path.exists(self.workspace_path):
            shutil.rmtree(self.workspace_path)
        os.makedirs(self.workspace_path)

    def clone_repo(self, repo_url: str):
        print(f"📥 Cloning {repo_url}...")
        self._clear_workspace()
        clean_url = repo_url.replace("https://", "")
        auth_url = f"https://{GITHUB_TOKEN}@{clean_url}"
        
        try:
            self.current_repo = Repo.clone_from(auth_url, self.workspace_path)
            with self.current_repo.config_writer() as git_config:
                git_config.set_value('user', 'email', 'agent@resurrector.bot')
                git_config.set_value('user', 'name', 'Resurrector Agent')
            return f"✅ Cloned {repo_url}"
        except Exception as e:
            return f"❌ Clone failed: {e}"

    def create_branch(self, branch_name="fix/auto-repair"):
        try:
            current = self.current_repo.create_head(branch_name)
            current.checkout()
            return f"🌿 Switched to branch: {branch_name}"
        except Exception as e:
            return f"❌ Branch failed: {e}"

    def commit_and_push(self, message="Fix applied by Resurrector Agent"):
        try:
            self.current_repo.git.add(A=True)
            self.current_repo.index.commit(message)
            origin = self.current_repo.remote(name='origin')
            branch = self.current_repo.active_branch
            origin.push(refspec=f'{branch}:{branch}')
            return "🚀 Changes pushed to GitHub"
        except Exception as e:
            return f"❌ Push failed: {e}"

    def create_pr(self, repo_full_name, title, body):
        try:
            repo = self.github_client.get_repo(repo_full_name)
            pr = repo.create_pull(
                title=title,
                body=body,
                head=str(self.current_repo.active_branch),
                base="main" 
            )
            return f"🎉 PR Created: {pr.html_url}"
        except Exception as e:
            return f"❌ PR failed: {e}"