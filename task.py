import spacy
import csv

nlp = spacy.load("en_core_web_sm")

# Function to extract action items from meeting transcripts
def extract_action_items(transcript, timestamp):
    doc = nlp(transcript)
    action_items = []
    for sentence in doc.sents:
        sentence_text = sentence.text
        if "action" in sentence_text.lower() or "task" in sentence_text.lower():
            action_items.append({"text": sentence_text, "assignee": "UNKNOWN", "ts": timestamp})
    return action_items

# Read the meeting transcript CSV file
with open("meeting_transcript.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        transcript_text = row["text"]
        timestamp = row["start_time"]
        action_items = extract_action_items(transcript_text, timestamp)
        for action_item in action_items:
            print(action_item)
