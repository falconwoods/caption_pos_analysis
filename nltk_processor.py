import json
import os
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag

# Download NLTK data (if not already downloaded)
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Define NLTK part-of-speech tags
NLTK_TAGS = {
    'CC': 'CC',
    'CD': 'CD',
    'DT': 'DT',
    'EX': 'EX',
    'FW': 'FW',
    'IN': 'IN',
    'JJ': 'JJ',
    'JJR': 'JJR',
    'JJS': 'JJS',
    'LS': 'LS',
    'MD': 'MD',
    'NN': 'NN',
    'NNS': 'NNS',
    'NNP': 'NNP',
    'NNPS': 'NNPS',
    'PDT': 'PDT',
    'POS': 'POS',
    'PRP': 'PRP',
    'PRP$': 'PRP$',
    'RB': 'RB',
    'RBR': 'RBR',
    'RBS': 'RBS',
    'RP': 'RP',
    'SYM': 'SYM',
    'TO': 'TO',
    'UH': 'UH',
    'VB': 'VB',
    'VBD': 'VBD',
    'VBG': 'VBG',
    'VBN': 'VBN',
    'VBP': 'VBP',
    'VBZ': 'VBZ',
    'WDT': 'WDT',
    'WP': 'WP',
    'WP$': 'WP$',
    'WRB': 'WRB',
    '$': '$',
    "''": "''",
    '(': '(',
    ')': ')',
    ',': ',',
    '--': '--',
    '.': '.',
    ':': ':',
    '``': '``'
}

# Rest of your code remains the same...


# Rest of your code remains the same...


# Function to read and parse the subtitle file
def read_subtitle_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        subtitle_text = file.read()
    return subtitle_text

# Function to analyze part of speech for each sentence and save to JSON
def analyze_subtitle(subtitle_text, output_file_path):
    subtitle_entries = subtitle_text.strip().split("\n\n")

    result_data = {"pos": []}

    for entry in subtitle_entries:
        lines = entry.strip().split("\n")
        if len(lines) >= 3:
            line_number = lines[0]
            time_stamp = lines[1]
            sentence = " ".join(lines[2:])

            # Tokenize the sentence
            tokens = word_tokenize(sentence)
            
            # Perform part-of-speech tagging
            pos_tags = {i: NLTK_TAGS[tag] for i, (_, tag) in enumerate(pos_tag(tokens))}
            print(line_number, [f"{token}={pos_tags[i]}" for i, token in enumerate(tokens)])

            result_data["pos"].append(pos_tags)

    # Save the result data to a JSON file
    with open(output_file_path, "w", encoding="utf-8") as json_file:
        json.dump(result_data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Directory path
    directory = "./srt"
    outputDir = "./output/nltk"

    # Create the output directory if it doesn't exist
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    # List to store .srt files
    srt_files = []

    # Iterate through files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".srt"):
            srt_files.append(os.path.join(directory, filename))

    # Now, srt_files contains the paths to all .srt files in the "./srt" directory
    # You can iterate through them or perform other operations as needed
    for srt_file in srt_files:
        print(srt_file)
        subtitle_text = read_subtitle_file(srt_file)
        output_file_path = os.path.join(outputDir, os.path.basename(srt_file).replace('.srt', '.json'))
        analyze_subtitle(subtitle_text, output_file_path)
