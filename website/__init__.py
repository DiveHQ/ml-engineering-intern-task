import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import spacy.cli


def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)

    spacy.cli.download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)

    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    # Max Frequency
    max_freq = max(word_freq.values())

    # Normalizing the frequency
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    # Sentence tokenization
    sent_tokens = [sent for sent in doc.sents]

    # Sentence Scores
    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    # Summary things
    select_len = int(len(sent_tokens) * 0.25)
    summary = nlargest(select_len, sent_scores, key = sent_scores.get)
    final_summary = [word.text for word in summary]
    print(final_summary)
    summary = ' '.join(final_summary)

    return summary, doc

def extract_action_items(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Initialize a list to store the extracted action items
    action_items = []

    # Iterate through each sentence in the document
    for sentence in doc.sents:
        # Initialize variables to store the assignee and important words in the sentence
        assignee = "UNKNOWN"
        important_words = []

        # Iterate through each token in the sentence
        for token in sentence:
            # Check if the token is a proper noun (potential assignee)
            if token.pos_ == "PROPN":
                assignee = token.text

                # Check if the token is a noun or a verb
            if token.pos_ in ["NOUN", "VERB"]:
                # Append the lemma of the token to the important words list
                important_words.append(token.lemma_)

        # Combine the important words into a sentence
        extracted_text = " ".join(important_words)

        # Append the extracted text and assignee to the action items list
        if extracted_text:
            action_items.append({"text": extracted_text, "assignee": assignee})

    return action_items, doc
