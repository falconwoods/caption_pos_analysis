import spacy
from spacy.tokenizer import Tokenizer
from spacy.util import compile_infix_regex
import json
import os

# Load the spaCy model for the English language
nlp = spacy.load("en_core_web_sm")

PosTags = {
    "NO_TAG": 1,
    "ADJ": 2,
    "ADP": 3,
    "ADV": 4,
    "AUX": 5,
    "CONJ": 6,
    "CCONJ": 6,
    "DET": 8,
    "INTJ": 9,
    "NOUN": 10,
    "NUM": 11,
    "PART": 12,
    "PRON": 13,
    "PROPN": 14,
    "PUNCT": 15,
    "SCONJ": 16,
    "SYM": 17,
    "VERB": 18,
    "X": 19,
    "EOL": 20,
    "SPACE": 21,
}

def custom_tokenizer(nlp):
    # Define the infix pattern without hyphen to prevent splitting hyphenated words
    infixes = (
        spacy.lang.char_classes.LIST_ELLIPSES
        + spacy.lang.char_classes.LIST_ICONS
        + [
            r"(?<=[0-9])[+\-\*^](?=[0-9-])",
            r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                al=spacy.lang.char_classes.ALPHA_LOWER,
                au=spacy.lang.char_classes.ALPHA_UPPER,
                q=spacy.lang.char_classes.CONCAT_QUOTES,
            ),
            r"(?<=[{a}]),(?=[{a}])".format(a=spacy.lang.char_classes.ALPHA),
            r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=spacy.lang.char_classes.ALPHA),
        ]
    )

    infix_re = compile_infix_regex(infixes)

    # Create a custom tokenizer with the modified infix pattern
    return Tokenizer(
        nlp.vocab,
        prefix_search=nlp.tokenizer.prefix_search,
        suffix_search=nlp.tokenizer.suffix_search,
        infix_finditer=infix_re.finditer,
        token_match=nlp.tokenizer.token_match,
        rules=nlp.Defaults.tokenizer_exceptions,
    )


# Set the custom tokenizer in the spaCy pipeline
nlp.tokenizer = custom_tokenizer(nlp)


# Function to read and parse the subtitle file
def read_subtitle_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        subtitle_text = file.read()
    return subtitle_text


# Function to analyze part of speech for each sentence and save to JSON
def analyze_subtitle(subtitle_text, output_file_path):
    subtitle_entries = subtitle_text.strip().split("\n\n")

    # result_data = {"pos": {}}
    result_data = {"pos": []}

    for entry in subtitle_entries:
        lines = entry.strip().split("\n")
        if len(lines) >= 3:
            line_number = lines[0]
            time_stamp = lines[1]
            sentence = " ".join(lines[2:])

            # Process the sentence
            sentence_doc = nlp(sentence)

            # Extract part of speech tags
            pos_tags = {}
            for token in sentence_doc:
                pos_tags[token.idx] = PosTags[token.pos_]
            print(line_number, [f"{token.text}={pos_tags[token.idx]}" for token in sentence_doc])

            # result_data["pos"][line_number].append(pos_tags)
            result_data["pos"].append(pos_tags)

    # Save the result data to a JSON file
    with open(output_file_path, "w", encoding="utf-8") as json_file:
        json.dump(result_data, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # Directory path
    directory = "./srt"
    outputDir = "./output/spacy"

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


