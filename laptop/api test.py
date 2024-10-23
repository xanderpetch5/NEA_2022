import csv

input_file = 'output.csv'
output_file = 'without repeats.csv'

# Use a set to keep track of seen rows
seen_rows = set()

# Open the input and output files
with open(input_file, 'r', newline='') as in_file, \
        open(output_file, 'w', newline='') as out_file:
    reader = csv.reader(in_file)
    writer = csv.writer(out_file)

    # Write the header row to the output file
    header = next(reader)
    writer.writerow(header)

    # Process each row in the input file
    total_rows = len(list(reader))
    in_file.seek(0)  # Reset file pointer to start
    next(reader)  # Skip header row
    for i, row in enumerate(reader, start=1):
        # Convert the row to a tuple to make it hashable
        row_tuple = tuple(row)
        # If the row has not been seen before, write it to the output file
        if row_tuple not in seen_rows:
            writer.writerow(row)
            seen_rows.add(row_tuple)

        # Calculate and display progress
        percent_complete = i / total_rows * 100
        print(f"Progress: {percent_complete:.2f}%", end='\r')

    # Print 100% progress when done
    print(f"Progress: 100.00%")
