import os
import getpass
import subprocess
from git import Repo, GitCommandError

def set_git_config(username, token):
    subprocess.run(["git", "config", "--global", "user.name", username])
    subprocess.run(["git", "config", "--global", "user.email", f"{username}@users.noreply.github.com"])
    subprocess.run(["git", "config", "--global", "credential.helper", "store"])
    # Store credentials in .git-credentials
    cred_path = os.path.expanduser("~/.git-credentials")
    with open(cred_path, "w") as f:
        f.write(f"https://{username}:{token}@github.com\n")

def update_remote_url(username, token, repo):
    origin_url = repo.remotes.origin.url
    # Remove embedded token (if exists)
    if "@" in origin_url:
        clean_url = origin_url.replace("https://", "").split("@")[-1]
        clean_url = "https://" + clean_url
    else:
        clean_url = origin_url
    # Rebuild with new token
    new_url = f"https://{username}:{token}@{clean_url[8:]}"  # strip "https://"
    repo.remotes.origin.set_url(new_url)
    print(f"✔️ Remote URL set to: {new_url}")

def choose_branch(repo):
    print("1. Use existing branch")
    print("2. Create new branch")
    choice = input("Choose (1/2): ").strip()
    if choice == "1":
        print("Available branches:")
        for b in repo.branches:
            print(" -", b)
        branch = input("Branch to use: ").strip()
        try:
            repo.git.checkout(branch)
        except GitCommandError:
            print(f"❌ Branch {branch} does not exist.")
            exit(1)
    else:
        cur = repo.active_branch.name
        new = input("New branch name: ").strip()
        repo.git.checkout("-b", new)
        branch = new
    print(f"✔️ Using branch: {branch}")
    return branch

def main():
    repo = Repo(os.getcwd())
    # Input credentials
    print("🔐 Enter GitHub token:")
    token = getpass.getpass()
    username = input("👤 Enter GitHub username: ").strip()
    set_git_config(username, token)
    update_remote_url(username, token, repo)

    # Branch selection
    branch = choose_branch(repo)

    # Commit changes
    msg = input("📝 Commit message: ").strip()
    repo.git.add(".")
    repo.git.commit("-m", msg)

    # Ask whether to push
    push_choice = input(f"🚀 Do you want to push to origin/{branch}? (yes/no): ").strip().lower()
    if push_choice in ["yes", "y"]:
        print(f"🔄 Pushing to origin/{branch}...")
        repo.git.push("-u", "origin", branch)
        print("✅ Push complete!")
    else:
        print("❌ Skipping push.")

if __name__ == "__main__":
    main()
