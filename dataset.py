import csv

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

generate("test.txt", "text.tsv")
