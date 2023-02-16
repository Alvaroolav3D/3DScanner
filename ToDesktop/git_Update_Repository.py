import os
import subprocess

# Define the repository name and URL
repo_name = "3DScanner"
repo_path = "/home/pi/Desktop/" + repo_name
repo_url = "https://github.com/Alvaroolav3D/3DScanner.git"

# Check if git is installed
try:
    subprocess.run(["git", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except subprocess.CalledProcessError:
    # If not installed, install git
    print("Installing git...")
    os.system("sudo apt-get update && sudo apt-get install git -y")

# Check if the repository exists locally
if not os.path.exists(repo_path):
    # Create the repository directory if it doesn't exist
    os.makedirs(repo_path, exist_ok=True)
    # Clone the repository
    print("Cloning repository...")
    subprocess.run(["git", "clone", repo_url, repo_path])

# Change to the repository directory
print("Changing to repository directory...")
os.chdir(repo_path)

# Fetch the latest updates from Github
print("Fetching updates...")
subprocess.run(["git", "fetch", "origin"])

# Check if the local repository is up-to-date
result = subprocess.run(["git", "diff", "HEAD", "origin/main"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Update the repository if there are new changes
if result.stdout or result.stderr:
    print("Updating repository...")
    subprocess.run(["git", "pull", "origin", "main"])
else:
    print("Repository is up-to-date.")
