import os
import shutil

def move_to_folder(filepath, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    filename = os.path.basename(filepath)
    target_path = os.path.join(target_dir, filename)

    if os.path.exists(target_path):
        base, ext = os.path.splitext(filename)
        i = 1
        while os.path.exists(os.path.join(target_dir, f"{base}_{i}{ext}")):
            i += 1
        target_path = os.path.join(target_dir, f"{base}_{i}{ext}")

    shutil.move(filepath, target_path)
