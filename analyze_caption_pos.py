import spacy
from spacy.tokenizer import Tokenizer
from spacy.util import compile_infix_regex
import json

# Load the spaCy model for the English language
nlp = spacy.load("en_core_web_sm")

PosTags = {
    "NO_TAG": 0,
    "ADJ": 1,
    "ADP": 2,
    "ADV": 3,
    "AUX": 4,
    "CONJ": 5,
    "CCONJ": 6,
    "DET": 7,
    "INTJ": 8,
    "NOUN": 9,
    "NUM": 10,
    "PART": 11,
    "PRON": 12,
    "PROPN": 13,
    "PUNCT": 14,
    "SCONJ": 15,
    "SYM": 16,
    "VERB": 17,
    "X": 18,
    "EOL": 19,
    "SPACE": 20,
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
            print(line_number, [token.text for token in sentence_doc])
            # result_data["pos"][line_number].append(pos_tags)
            result_data["pos"].append(pos_tags)

    # Save the result data to a JSON file
    with open(output_file_path, "w", encoding="utf-8") as json_file:
        json.dump(result_data, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    subtitle_file_path = "input.srt"
    subtitle_text = read_subtitle_file(subtitle_file_path)
    output_file_path = "output.json"
    analyze_subtitle(subtitle_text, output_file_path)
