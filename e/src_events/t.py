'''import csv

# Path of the input and output CSV files
input_file = 'a4.csv'
output_file = 'output.csv'

# Open input and output files
with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', newline='', encoding='utf-8') as f_out:
    reader = csv.DictReader(f_in)
    writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames)
    writer.writeheader()
    
    # Iterate over each row in the input file
    for row in reader:
        # Check if the text column is not empty
        if row['text'] != "" or row['label'] == "correct":
            # Write the row to the output file
            writer.writerow(row)
            print(row)  '''
import csv

# Path of the input and output CSV files
input_file = 'a4.csv'
output_file = 'output.csv'

# Open input and output files
with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', newline='', encoding='utf-8') as f_out:
    reader = csv.DictReader(f_in)
    writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames)
    writer.writeheader()
    
    # Iterate over each row in the input file
    for row in reader:
        # Check if the text column is not empty
        if row['text'] == "":
            row['text'] = row['semantic_rep']
        # Write the row to the output file
        writer.writerow(row)

