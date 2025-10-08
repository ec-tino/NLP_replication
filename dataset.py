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
        writer.writerow(["sentid", "pairid", "sent", "comparison"])
        sentid = 1  
        for i in range(0, len(lines), 2):
            pairid = i // 2 + 1
            for line in lines[i:i+2]:
                comparison, sent = line.split('\t', 1)
                writer.writerow([sentid, pairid, sent, comparison])
                sentid += 1  

file_names = get_file_names_in_folder("eval_file")

for name in file_names:
    # Remove the .txt extension
    base_name = os.path.splitext(name)[0]
    generate(f"eval_file/{name}", f"data_file/{base_name}.tsv")
