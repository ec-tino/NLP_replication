import csv
import os

def get_file_names_in_folder(folder_path):
    file_names = []
    if os.path.isdir(folder_path):
        for entry in os.listdir(folder_path):
            full_path = os.path.join(folder_path, entry)
            if os.path.isfile(full_path):
                file_names.append(entry)
    else:
        print(f"Error: '{folder_path}' is not a valid directory.")
    return file_names

def generate(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    with open(output_file, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(["sentid", "pairid", "sentence", "comparison"])
        sentid = 1
        for i in range(0, len(lines), 2):
            pairid = i // 2 + 1
            for line in lines[i:i+2]:
                comparison, sent = line.split('\t', 1)
                if comparison == "True":
                    comparison = "expected"
                else:
                    comparison = "unexpected"
                writer.writerow([sentid, pairid, sent, comparison])
                sentid += 1

# Root folder should be the one containing your language subfolders
root_folder = "language"

for lang_folder in os.listdir(root_folder):
    lang_path = os.path.join(root_folder, lang_folder)
    eval_path = os.path.join(lang_path, "eval_file")
    data_path = os.path.join(lang_path, "data_file")

    if not os.path.isdir(eval_path):
        continue

    # Create data_file folder if missing
    os.makedirs(data_path, exist_ok=True)

    file_names = get_file_names_in_folder(eval_path)

    for name in file_names:
        base_name = os.path.splitext(name)[0]
        input_file = os.path.join(eval_path, name)
        output_file = os.path.join(data_path, f"{base_name}.tsv")
        generate(input_file, output_file)
        print(f"✅ Processed: {lang_folder}/{base_name}.tsv")
