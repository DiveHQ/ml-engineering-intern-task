import re
import torch
from transformers import BertTokenizer, BertForSequenceClassification
# from transformers import RobertaTokenizer, RobertaForSequenceClassification
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def classify_action_item(text):
    inputs = tokenizer.encode_plus(text, add_special_tokens=True, truncation=True, padding='max_length', max_length=512, return_tensors='pt')
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']

    outputs = model(input_ids, attention_mask=attention_mask)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1).squeeze().tolist()
    predicted_label = torch.argmax(logits, dim=1).item()

    return predicted_label, probabilities
# Path: transcript_to_action_items.py
transcripts = [
    ["00:00:00", "00:00:15", "Alice", "Good afternoon, everyone!"],
    ["00:00:15", "00:00:40", "Bob", "Good afternoon, Alice. How was your weekend?"],
    ["00:00:40", "00:01:00", "Alice", "It was great, Bob. How about yours?"],
    ["00:01:00", "00:01:30", "Bob", "I had a relaxing weekend, thanks for asking."],
    ["00:01:30", "00:02:00", "Carol", "Hello, team! We have some exciting news to share."],
    ["00:02:00", "00:02:45", "Alice", "Hello, Carol. Please go ahead."],
    ["00:02:45", "00:03:30", "Carol", "We have secured a new client for our project!"],
    ["00:03:30", "00:04:00", "Bob", "That's fantastic, Carol! Who is the new client?"],
    ["00:04:00", "00:04:30", "Carol", "The new client is a leading tech company in our industry."],
    ["00:04:30", "00:05:00", "Alice", "That's a significant achievement for our team."],
    ["00:05:00", "00:05:30", "Carol", "Absolutely, Alice. We need to start preparations immediately."],
    ["00:05:30", "00:06:00", "Bob", "What's the timeline for the project, Carol?"],
    ["00:06:00", "00:06:30", "Carol", "We have six months to complete the project successfully."],
    ["00:06:30", "00:07:00", "Alice", "Let's ensure we allocate resources accordingly for a timely delivery."],
    ["00:07:00", "00:07:30", "Bob", "I'll coordinate with the development team to kickstart the project."],
    ["00:07:30", "00:08:00", "Carol", "Great! Let's have a follow-up meeting next week to discuss further details."],
    ["00:08:00", "00:08:15", "Alice", "Sounds good, Carol."],
    ["00:08:15", "00:08:30", "Bob", "I'll have a look at the project timeline shortly."],
    ["00:08:30", "00:08:45", "Carol", "Thanks, Bob. I'll see you all next week."],
    ["00:08:45", "00:09:00", "Alice", "Have a great day, everyone!"],
    ["00:09:00", "00:09:15", "Bob", "You too, Alice. See you next week."],
    ["00:09:15", "00:09:30", "Carol", "Have a great day, Alice."],
    ["00:09:30", "00:09:45", "Bob", "You too, Carol. See you next week."],
]

action_items = []
# Path: transcript_to_action_items.py

for transcript in transcripts:
    text = transcript[3]
    assignee = re.findall(r"([A-Za-z]+),", text)
    assignee = assignee[0] if assignee else "UNKNOWN"
    predicted_label, probabilities = classify_action_item(text)

    if predicted_label == 1:  # Action item predicted
        action_item = re.findall(r"[A-Za-z\s]+", text)
        action_item = action_item[0].strip() if action_item else ""

        if action_item:
            action_items.append({"text": action_item, "assignee": assignee, "ts": transcript[0]})

for item in action_items:
    print(item)




