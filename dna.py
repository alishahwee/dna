from csv import DictReader
from sys import argv, exit


def main():
    # Ensure proper use of program
    if len(argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        exit(1)

    # Open csv files and read into memory
    with open(argv[1], newline='') as database_f:
        database = DictReader(database_f)

        # Intialize a dict showing available STRs for analysis
        STR_dict = {STR: 0 for STR in database.fieldnames[1:]}  # STR starts at index 1 (name is at index 0)

        # Open sequence files and read into memory
        with open(argv[2], "r") as sequence_f:
            sequence = sequence_f.read()

            # Use STR from STR_dict and calculate count from sequence; update dict
            for STR in STR_dict.keys():
                STR_dict[STR] = count_STR(STR, sequence)

        # Compare STR_dict count with database and find any matches
        match = find_match(database, STR_dict)

        # Print results
        if match is None:
            print("No match")
        else:
            print(match)

    exit(0)


# Generator that returns indices where STR is found
def find_STR(STR, sequence):
    start = 0
    i = 0
    # Loop through sequence until starting index is less than STR length or until no matches
    while start < len(sequence) - len(STR) and i >= 0:
        i = sequence.find(STR, start)
        if i >= 0:
            yield i
        # Set starting index to the ending index of previous match
        start = i + len(STR)

# Define a function to count the length of short tandem repeats


def count_STR(STR, sequence):
    count = 0  # Official longest repeat
    curr_count = 1  # Initialized to include the first match
    STR_indices = list(find_STR(STR, sequence))  # Generator list of indices

    # Iterate through the index matches from generator
    for i in range(len(STR_indices) - 1):
        # If previous and next index match equals STR length, then it's a repeat
        if STR_indices[i + 1] - STR_indices[i] == len(STR):
            curr_count += 1
        # If repeat ends, compare the current count and replace official count if higher
        elif curr_count > count and len(STR_indices) > 0:
            count = curr_count
            curr_count = 1  # Reinitialize current count
    # If repeat not detected, but a match is listed, set count to 1
    if len(STR_indices) == 1:
        count = 1
    # Else if only one STR strand detected, set count
    elif curr_count > count and len(STR_indices) > 0:
        count = curr_count
    return count

# Identify who has the matching DNA


def find_match(database, STR_dict):
    match = None
    for person in database:
        for STR, count in STR_dict.items():
            # If there's any no-match, skip to the next person
            if int(person[STR]) != count:
                break
        else:
            match = person["name"]
            break
    return match


main()
