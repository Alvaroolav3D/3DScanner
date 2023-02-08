import sys

# Get the version of Python installed
version = sys.version_info[:3]

# Save the version as a string
version_str = ".".join(str(x) for x in version)

# Print the version
print("Python version:", version_str)