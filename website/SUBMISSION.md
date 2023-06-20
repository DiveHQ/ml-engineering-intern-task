
# Setup Codebase and Dependencies

### Generate csv file that contains trancripted text

    def generate_csv_data(speakers):
        """Generating CSV Data from (Hugging Face) knkarthick/AMI."""
        with open("output.csv", "w") as csv_file:
            csv_writer = csv.writer(csv_file)
            for speaker in speakers:
                start_time = speaker["start_time"]
                end_time = speaker["end_time"]
                text = speaker["text"]
                csv_writer.writerow([start_time, end_time, speaker["name"], text])

The above code defines a function called `generate_csv_data` that takes a list of speakers as input. The purpose of this function is to generate CSV data from the input speakers' information.

Here's a breakdown of what the code does:

1. It opens a file named "output.csv" in write mode using the `open()` function with the `"w"` mode specifier. This file will be used to store the generated CSV data.

2. It creates a CSV writer object called `csv_writer` using the `csv.writer()` function, which takes the opened file (`csv_file`) as an argument.

3. It iterates over each speaker in the `speakers` list using a `for` loop.

4. For each speaker, it retrieves the start time, end time, name, and text from the speaker's dictionary using the respective keys (`"start_time"`, `"end_time"`, `"name"`, and `"text"`).

5. It writes a row to the CSV file using the `csv_writer.writerow()` method. The row contains the start time, end time, speaker's name, and the text. These values are passed as a list (`[start_time, end_time, speaker["name"], text]`).

*Overall, this code generates a CSV file named "output.csv" and populates it with rows of data, where each row corresponds to a speaker and includes their start time, end time, name, and text.*


### Upload the csv file and extract text from it

    def upload_csv():
        if request.method == 'POST':
            file = request.files['file']
    
            if file and file.filename.endswith('.csv'):
                data = []
    
                # Read the CSV file
                stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                csv_data = csv.reader(stream)
                for row in csv_data:
                    data.append(row)
    
                return render_template('display_csv.html', data=data)
    
        return render_template('upload.html')

1. It checks if the HTTP request method is "POST".
2. If it is a "POST" request, it retrieves the file from the request using `request.files['file']`. The assumption here is that a file input field in an HTML form has the name "file".
3. It checks if the file has a ".csv" extension using file.filename.endswith('.csv').
4. If the file is a CSV file, it initializes an empty list called data. 
5. It reads the contents of the file and stores them in a `StringIO` object called stream. The contents are decoded as UTF-8.
6. It creates a CSV reader object called csv_data using the csv.reader() function, passing in the stream object.
7. It iterates over each row in csv_data and appends it to the data list.
8. Finally, it returns the data list to a template called `display_csv.html` using `render_template()`. The template is responsible for displaying the contents of the CSV file.
9. If the request method is not "POST" or the file is not a CSV file, it returns a template called `upload.html`, which likely contains an HTML form to upload a file.

### Extract the action items from the text column

    import spacy

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

The above code defines a function called `extract_action_items` that takes a text as input and uses the spaCy library to extract action items from the text. Here's how the code works:

1. It loads the English language model from spaCy using `en_core_web_sm`.
2. It processes the input text using the loaded language model, creating a `doc` object that represents the parsed text.
3. It initializes an empty list called `action_items` to store the extracted action items.
4. It iterates through each sentence in the document (`doc.sents`).
5. For each sentence, it initializes the variables `assignee` with a default value of "UNKNOWN" and `important_words` as an empty list.
6. It iterates through each token in the sentence.
7. If the token is identified as a proper noun (denoted by `token.pos_ == "PROPN"`), it is considered a potential assignee, and its text value is assigned to the `assignee` variable.
8. If the token's part-of-speech tag is either "NOUN" or "VERB", it is considered an important word. The lemma of the token (base form of the word) is appended to the `important_words` list.
9. After iterating through all tokens in the sentence, the `important_words` are joined together into a sentence using spaces, creating the `extracted_text`.
10. If `extracted_text` is not empty, it means that important words were found in the sentence. In this case, a dictionary containing the `text` and `assignee` is appended to the `action_items` list.
11. After processing all sentences, the function returns both the `action_items` list and the `doc` object representing the parsed text.

*In summary, this function aims to identify sentences containing important words (nouns or verbs) and extract those words as action items, along with a potential assignee if a proper noun is identified. The extracted action items are returned as a list of dictionaries, and the parsed text is returned as a spaCy `doc` object.*
### Running the pipeline

    def home():
    if request.method == 'POST':
        # Gets the note from the HTML
        note = request.form.get('note')
        # If note length is too short
        if len(note) < 1:
            flash('Text is too short!', category='error')
        # Minimum len for the model generation
        elif len(note) > 10:
            action_items, original_text = extract_action_items(note)
            flash(' Task Done!', category='success')
            return render_template("nlp_model.html", action_items = action_items, original_text = original_text)

    return render_template("home.html")


Here is a breakdown of what the code does:
1. It checks the `HTTP` method used to access the endpoint. If the method is "POST," it proceeds with the code inside the if block. Otherwise, it skips to the last line and renders the "home.html" template. 
2. Inside the if block, it retrieves the value of a form field named `note` using `request.form.get('note')`. This assumes that the code is running within a web framework that provides the request object for handling HTTP requests. 
3. It then checks the length of the text. If the length is less than 1, it flashes an error message using `flash()` function with the category set to 'error'. 
4. If the length of the text is greater than 10, it calls the `extract_action_items()` function, passing the note as an argument. It assumes that the extract_action_items() function is defined elsewhere and returns two values: action_items and original_text. 
5. After extracting the action items, it flashes a success message using flash() with the category set to `success`. 
6. Finally, it renders the "nlp_model.html" template, passing action_items and original_text as variables. 
7. If the HTTP method is not `POST` the function simply renders the `home.html` template.






### [Optional]: Summarize the text column 


The function "summarizer" takes a raw document as input and returns a summary of the document. It utilizes the spaCy library for natural language processing.
Here is a breakdown of what the code does:
1. Imports necessary modules and functions:
spacy.lang.en.stop_words imports the list of stop words from `spaCy's` English language module.
`string.punctuation` imports a string containing all the punctuation marks.
`heapq.nlargest` is used to find the N largest elements from a collection.
2. Defines the summarizer function that takes a rawdocs parameter.
3. Initializes a list of stop words using spaCy's predefined stop words.
4. Loads the English language model using `spacy.load('en_core_web_sm')`.
4. Processes the rawdocs by passing it to the loaded spaCy model. The processed document is stored in the variable doc.
5. Initializes an empty dictionary `word_freq` to store the frequency of each word.
6. Iterates over each word in the processed document doc and checks if it is not a stop word and not a punctuation mark. If the conditions are satisfied, it updates the word_freq dictionary by either adding a new key with a frequency of 1 or incrementing the frequency if the word already exists as a key.
7. Tokenizes the document into sentences and stores them in the list sent_tokens. 
8. Initializes an empty dictionary sent_scores to store the scores of each sentence. 
9. Iterates over each sentence in `sent_tokens` and for each word in the sentence, it checks if the word exists in `word_freq`. If it does, it adds the corresponding frequency to the sentence's score in the sent_scores dictionary. If the word's part of speech is `"PROPN"` (proper noun), it assigns the sentence's text to the variable assignee. 
10. Selects the length of the summary by calculating 5% of the total number of sentences and storing it in the variable select_len. 
11. Uses the nlargest function to extract the select_len number of sentences with the highest scores from `sent_scores`. The sentences are stored in the summary variable as a list of spaCy Span objects. 
12. Extracts the text of each sentence in summary and stores them in the `final_summary list`. 
13. Prints the final_summary list. 
14. Joins the elements of final_summary into a string with spaces between them and assigns it to the summary variable. 
15. Returns the summary string, the processed document doc.

*The "summarizer" function utilizes spaCy's natural language processing capabilities to generate a summary of a given raw document. It first processes the document by removing stop words and punctuation, and then calculates the frequency of each word. The sentences in the document are tokenized and assigned scores based on the frequencies of their constituent words. The function selects a subset of sentences with the highest scores to form the summary. Finally, it returns the summary as a string along with the processed document. In summary, the function leverages spaCy's functionality to extract key sentences from the document, resulting in a concise summary.*

