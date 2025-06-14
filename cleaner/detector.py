import os
from PIL import Image
import imagehash

def find_similar_images(directory, threshold=5):
    hashes = {}
    groups = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        try:
            img = Image.open(filepath)
            h = imagehash.average_hash(img)

            found_group = False
            for k in hashes:
                if abs(h - k) <= threshold:
                    hashes[k].append(filepath)
                    found_group = True
                    break

            if not found_group:
                hashes[h] = [filepath]

        except Exception as e:
            print(f"❌ Skipped {filename}: {e}")

    return [group for group in hashes.values() if len(group) > 1]
