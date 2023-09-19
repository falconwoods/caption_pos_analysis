import re

# Define regular expressions for extracting data
word_pattern = re.compile(r'^(\w+)\s+(<[^>]*>)*$')
meaning_pattern = re.compile(r'^\s*([^\s].*)$')

# Initialize variables to store extracted data
entries = []

# Open and read the MDX dictionary text file
with open('oxford.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

current_entry = None

# Iterate through lines to extract data
for line in lines:
    word_match = word_pattern.match(line)
    meaning_match = meaning_pattern.match(line)

    if word_match:
        # Start a new entry
        if current_entry:
            entries.append(current_entry)
        word = word_match.group(1)
        current_entry = {"word": word, "meanings": []}
    elif meaning_match and current_entry:
        # Add meaning to the current entry
        meaning = meaning_match.group(1)
        current_entry["meanings"].append(meaning)

# Add the last entry (if any)
if current_entry:
    entries.append(current_entry)

# Print extracted words and their meanings
for entry in entries:
    print(f"Word: {entry['word']}")
    print("Meanings:")
    for meaning in entry['meanings']:
        print(f"  - {meaning}")
    print("\n")
