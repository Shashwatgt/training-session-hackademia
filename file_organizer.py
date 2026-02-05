import os

# -------------------------------
# 1) CONFIG
# -------------------------------
DRY_RUN = True  # Change to False to actually move files

# If you're in a .py script, __file__ exists.
# If you're in a notebook/interactive, __file__ does NOT exist.
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folder where the script is located
except NameError:
    BASE_DIR = os.getcwd()  # folder where the notebook/kernel is running

# The dataset folder you want to organize
DATASET_DIR = os.path.join(BASE_DIR, "hackademia")

# -------------------------------
# 2) CATEGORY RULES
# -------------------------------
CATEGORIES = {
    "pdfs": [".pdf"],
    "csv": [".csv"],
    "images": [".jpg", ".jpeg", ".png"],
    "texts": [".txt", ".md"],
}

# Any file not matching above goes to "others"
DEFAULT_CATEGORY = "others"

# -------------------------------
# 3) CREATE DESTINATION FOLDERS
# -------------------------------
# We create all category folders inside DATASET_DIR
all_folders = list(CATEGORIES.keys()) + [DEFAULT_CATEGORY]

for folder_name in all_folders:
    folder_path = os.path.join(DATASET_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)

# -------------------------------
# 4) MOVE FILES + TRACK COUNTS
# -------------------------------
counts = {folder: 0 for folder in all_folders}
moved_files_log = []  # store what we moved for the report

# list everything in dataset folder
for item in os.listdir(DATASET_DIR):
    src_path = os.path.join(DATASET_DIR, item)

    # Skip folders (important!)
    if not os.path.isfile(src_path):
        continue

    # Skip the report file if it already exists
    if item == "report.txt":
        continue

    # Figure out file extension
    _, ext = os.path.splitext(item)
    ext = ext.lower()

    # Decide category
    category = DEFAULT_CATEGORY
    for cat_name, ext_list in CATEGORIES.items():
        if ext in ext_list:
            category = cat_name
            break

    # Build destination path
    dest_path = os.path.join(DATASET_DIR, category, item)

    # -------------------------------
    # Safety: handle name collision
    # -------------------------------
    # If a file with same name exists in destination, rename it:
    # example: file.pdf -> file_1.pdf
    if os.path.exists(dest_path):
        name, extension = os.path.splitext(item)
        i = 1
        while True:
            new_name = f"{name}_{i}{extension}"
            dest_path = os.path.join(DATASET_DIR, category, new_name)
            if not os.path.exists(dest_path):
                break
            i += 1

    # Move (or dry run)
    action = f"MOVE: {src_path}  -->  {dest_path}"
    if DRY_RUN:
        print("[DRY RUN]", action)
    else:
        os.rename(src_path, dest_path)
        print(action)

    # Track stats (count it even in dry run so report is still meaningful)
    counts[category] += 1
    moved_files_log.append((item, category))

# -------------------------------
# 5) WRITE REPORT
# -------------------------------
report_path = os.path.join(DATASET_DIR, "report.txt")

total_moved = sum(counts.values())

lines = []
lines.append("DATASET ORGANIZER REPORT\n")
lines.append(f"Base Directory Used: {BASE_DIR}\n")
lines.append(f"Dataset Directory: {DATASET_DIR}\n")
lines.append(f"DRY_RUN Mode: {DRY_RUN}\n")
lines.append(f"Total Files Processed: {total_moved}\n\n")

lines.append("Files moved per category:\n")
for folder in all_folders:
    lines.append(f"  - {folder}: {counts[folder]}\n")

lines.append("\nMoved file list:\n")
for filename, category in moved_files_log:
    lines.append(f"  - {filename}  -->  {category}/\n")

# In dry run, we can still write the report (that’s fine)
with open(report_path, "w") as f:
    f.writelines(lines)

print(f"\nReport written to: {report_path}")
