import spacy

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

def extract_text_from_txt(file_path):
    """
    Extracts text from a .txt file.
    :param file_path: Path to the .txt file.
    :return: Extracted text from the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def summarize_text_spacy(text):
    """
    Summarizes text by extracting the top 3 important sentences using spaCy.
    :param text: The text to summarize.
    :return: A summarized version of the text (3 sentences).
    """
    doc = nlp(text)
    
    # Extract sentences based on Named Entities or keywords
    important_sentences = []

    # Look for sentences with named entities (people, organizations, etc.)
    for sent in doc.sents:
        if len([ent for ent in sent.ents]) > 0:  # If sentence contains any named entity
            important_sentences.append(sent.text)

    # If not enough sentences with named entities, select the longest sentences
    if len(important_sentences) < 3:
        sorted_sentences = sorted(doc.sents, key=lambda sent: len(sent), reverse=True)
        important_sentences.extend([sent.text for sent in sorted_sentences[:3 - len(important_sentences)]])

    # Return the top 3 sentences as a summary
    summary = ' '.join(important_sentences[:3])  # Limit to 3 sentences
    return summary

# Specify the path to your .txt file
file_path = '/Users/paidi.saimani/Desktop/std/uploads/resources/hello.txt'

# Extract the text from the .txt file
text = extract_text_from_txt(file_path)

# Perform summarization using spaCy
summary = summarize_text_spacy(text)

# Print the summarized text (3 lines)
print("Summarized Text: ", summary)
