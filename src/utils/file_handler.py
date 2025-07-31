def read_file(file_path):
    """Reads the content of a file and returns it."""
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, data):
    """Writes data to a file."""
    with open(file_path, 'w') as file:
        file.write(data)