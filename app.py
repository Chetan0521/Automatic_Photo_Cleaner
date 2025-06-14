from cleaner.detector import find_similar_images
from cleaner.face_quality import score_image
from cleaner.utils import move_to_folder
import os
import csv


INPUT_DIR = "images"
OUTPUT_DIR = "cleaned"
DELETED_DIR = "deleted"

def main():
    print("🔍 Scanning for similar images...")
    groups = find_similar_images(INPUT_DIR)

    log_path = "log.csv"
    with open(log_path, mode='w', newline='') as logfile:
        writer = csv.writer(logfile)
        writer.writerow(["Group", "Image", "Score", "Status"])

        if not groups:
            print("No duplicates found.")
            return

        for i, group in enumerate(groups, 1):
            print(f"\n📸 Group {i}: {len(group)} similar images")
            scores = {img: score_image(img) for img in group}

            best = max(scores, key=scores.get)
            print(f"✔ Best image: {os.path.basename(best)} (Score: {scores[best]:.2f})")
            move_to_folder(best, OUTPUT_DIR)
            writer.writerow([i, best, scores[best], "Selected"])

            for img in group:
                if img != best:
                    move_to_folder(img, DELETED_DIR)
                    writer.writerow([i, img, scores[img], "Rejected"])

    print("\n✅ Cleaning complete! Log saved as log.csv.")


if __name__ == "__main__":
    main()
