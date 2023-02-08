import os
import subprocess

# Check if git is installed
try:
    subprocess.run(["git", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except subprocess.CalledProcessError:
    # If not installed, install git
    print("Installing git...")
    os.system("sudo apt-get update && sudo apt-get install git -y")

# Define the repository name and URL
repo_name = "3DScanner"
repo_url = "https://github.com/Alvaroolav3D/3DScanner.git"

# Check if the repository exists locally
if not subprocess.run(["test", "-d", repo_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
    # Clone the repository if it doesn't exist
    print("Cloning repository...")
    subprocess.run(["git", "clone", repo_url])

# Change to the repository directory
print("Changing to repository directory...")
subprocess.run(["cd", repo_name])

# Fetch the latest updates from Github
print("Fetching updates...")
subprocess.run(["git", "fetch", "origin"])

# Check if the local repository is up-to-date
result = subprocess.run(["git", "diff", "HEAD", "origin/master"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Update the repository if there are new changes
if result.stdout or result.stderr:
    print("Updating repository...")
    subprocess.run(["git", "pull", "origin", "master"])
else:
    print("Repository is up-to-date.")