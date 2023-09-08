import os

def remove_jpg_files(path):
    for filename in os.listdir(path):
        if filename.endswith(".jpg"):
            file_path = os.path.join(path, filename)
            os.remove(file_path)
            print(f"Deleted: {filename}")
