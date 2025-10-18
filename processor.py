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
        # new columns for ROI
        writer.writerow(["sentid", "pairid", "sentence", "comparison", "ROI", "word"])
        sentid = 1

        for i in range(0, len(lines), 2):
            pairid = i // 2 + 1
            if i >= len(lines):
                print(f"Skipped incomplete pair in {input_file}")
            line1, line2 = lines[i:i+2]
            
            comp1, sent1 = line1.split('\t', 1)
            comp2, sent2 = line2.split('\t', 1)

            comp1 = "expected" if comp1.lower() == "true" else "unexpected"
            comp2 = "expected" if comp2.lower() == "true" else "unexpected"

            # tokenize by whitespace
            tokens1 = sent1.split()
            tokens2 = sent2.split()

            # find first different token
            roi_idx = -1
            for j in range(min(len(tokens1), len(tokens2))):
                if tokens1[j] != tokens2[j]:
                    roi_idx = j
                    break
            # if length different, first difference is at end 
            if roi_idx == -1:
                roi_idx = min(len(tokens1), len(tokens2)) - 1

            roi_tok1 = tokens1[roi_idx] if 0 <= roi_idx < len(tokens1) else ""
            roi_tok2 = tokens2[roi_idx] if 0 <= roi_idx < len(tokens2) else ""

            roi_tok1 = roi_tok1.split("##")[0]
            roi_tok2 = roi_tok2.split("##")[0]

            writer.writerow([sentid, pairid, sent1, comp1, roi_idx, roi_tok1]); sentid += 1
            writer.writerow([sentid, pairid, sent2, comp2, roi_idx, roi_tok2]); sentid += 1


# Root folder containing your language folders
root_folder = "language"

for lang_folder in os.listdir(root_folder):
    lang_path = os.path.join(root_folder, lang_folder)
    eval_path = os.path.join(lang_path, "eval_file")
    data_path = os.path.join(lang_path, "data_file")

    if not os.path.isdir(eval_path):
        continue

    os.makedirs(data_path, exist_ok=True)
    file_names = get_file_names_in_folder(eval_path)

    for name in file_names:
        base_name = os.path.splitext(name)[0]
        input_file = os.path.join(eval_path, name)
        output_file = os.path.join(data_path, f"{base_name}.tsv")
        generate(input_file, output_file)
        print(f"✅ Processed: {lang_folder}/{base_name}.tsv")
