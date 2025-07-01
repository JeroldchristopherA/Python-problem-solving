import os
import getpass
import subprocess
from git import Repo, GitCommandError

def set_git_config(username, token):
    subprocess.run(["git", "config", "--global", "user.name", username], check=True)
    subprocess.run(["git", "config", "--global", "user.email", f"{username}@users.noreply.github.com"], check=True)
    subprocess.run(["git", "config", "--global", "credential.helper", "store"], check=True)
    cred_path = os.path.expanduser("~/.git-credentials")
    with open(cred_path, "w") as f:
        f.write(f"https://{username}:{token}@github.com\n")

def update_remote_url(username, token, repo):
    origin_url = repo.remotes.origin.url
    if origin_url.startswith("https://github.com/"):
        clean_url = origin_url[len("https://"):]
    else:
        raise Exception(
            f"❌ Unexpected remote URL format: {origin_url}\n"
            f"Please run: git remote set-url origin https://github.com/<user>/<repo>.git"
        )
    new_url = f"https://{username}:{token}@{clean_url}"
    repo.remotes.origin.set_url(new_url)
    print(f"✔️ Remote URL set to: {new_url}")

def choose_branch(repo):
    while True:
        print("Available branches:")
        for b in repo.branches:
            print(" -", b)
        branch = input("Enter branch to switch to (or type 'new' to create): ").strip()
        if branch == "new":
            new = input("New branch name: ").strip()
            try:
                repo.git.checkout("-b", new)
                branch = new
                print(f"✔️ Created and switched to branch: {branch}")
                return branch
            except GitCommandError:
                print(f"❌ Could not create branch {new}. Try another name.")
        else:
            try:
                repo.git.checkout(branch)
                print(f"✔️ Switched to branch: {branch}")
                return branch
            except GitCommandError:
                print(f"❌ Branch {branch} does not exist. Try again or type 'new' to create.")

def select_files_to_commit(repo):
    changed_files = [item.a_path for item in repo.index.diff(None)]
    untracked_files = repo.untracked_files
    print("\nModified files:")
    for i, f in enumerate(changed_files, 1):
        print(f"  {i}. {f}")
    print("Untracked files:")
    for i, f in enumerate(untracked_files, 1):
        print(f"  {i+len(changed_files)}. {f}")
    all_files = changed_files + untracked_files
    if not all_files:
        print("Nothing to commit.")
        return []
    to_commit = input("Enter file numbers to add (comma-separated), or 'all' to add all: ").strip()
    if to_commit.lower() == "all":
        return all_files
    indices = [int(i)-1 for i in to_commit.split(",") if i.strip().isdigit()]
    selected = [all_files[i] for i in indices if 0 <= i < len(all_files)]
    print("Files to commit:", selected)
    return selected

def main():
    try:
        repo = Repo(os.getcwd())
    except Exception:
        print("❌ This directory is not a git repository. Please run this script from the root of your git repo.")
        exit(1)

    print("🔐 Enter GitHub token:")
    token = getpass.getpass()
    username = input("👤 Enter GitHub username: ").strip()
    set_git_config(username, token)
    update_remote_url(username, token, repo)

    branch = choose_branch(repo)

    files_to_add = select_files_to_commit(repo)
    if not files_to_add:
        print("⚠️ No files selected for commit. Exiting.")
        return

    for f in files_to_add:
        repo.git.add(f)
    msg = input("📝 Commit message: ").strip()
    try:
        repo.git.commit("-m", msg)
    except GitCommandError as e:
        if "nothing to commit" in str(e):
            print("⚠️ Nothing to commit. No changes staged.")
        else:
            raise

    push_choice = input(f"🚀 Do you want to push to origin/{branch}? (yes/no): ").strip().lower()
    if push_choice in ["yes", "y"]:
        print(f"🔄 Pushing to origin/{branch}...")
        repo.git.push("-u", "origin", branch)
        print("✅ Push complete!")
    else:
        print("❌ Skipping push.")

if __name__ == "__main__":
    main()
