# Code Setup and Pipeline Execution
### Setting Up the Codebase
- Ensure that you have Python installed on your system.

- Fork the repository and clone it into your local system.

- Open a terminal or command prompt and navigate to the directory that stores the codebase and run main.py into your Python IDE (PyCharm Professional Preferred).

### Approaches Considered:
When building an NLP model, there are several approaches that can be considered, including but not limited to:

- Generated the CSV data manually from the (Hugging Face) knkarthick/AMI [ consists of more than 100 hours of transcripted meetings] as it uses lots of computational power due to lots of noise and outliers in data. So for the demo used the manually generated csv.
- Load the pre-trained English language model from spaCy.
- Define the function extract_action_items that takes a text as input.Tokenize the text using spaCy's nlp object.
- Iterate through each sentence in the tokenized text.
- Initialize variables to store the assignee and important words in the sentence.
- Iterate through each token in the sentence and check for proper nouns (potential assignees) and important words (nouns or verbs).
- Append the lemma of the important tokens to the important_words list.Combine the important words into a sentence. And finally append the extracted text and assignee it to the action_items list.
- Return the action_items list.
- Provide an example transcript, call the extract_action_items function on the transcript, and print the extracted action items with their assignees.

### Assumptions Made:
The assumptions made during the NLP model generation process includes:

- **Data quality**: Assuming that the provided data is properly labeled, transcripted, and free from significant noise or bias.

- **Language and domain**: Assuming that the NLP model will be applied to text written in a specific language and domain. NLP models trained on one language or domain may not perform well on others.

- **Feature representation**: Assuming that the chosen feature representation methods, such as Spacy and its pretrained English language model called "en_core_web_sm", adequately capture the semantics and context of the text.


### Spacy for the Development of the NLP Model:
- Efficient Processing: SpaCy is known for its speed and efficiency in processing large volumes of text data. It can handle real-time or high-throughput applications effectively, making it suitable for tasks that involve processing a large number of documents or messages.
- Linguistic Features: SpaCy provides a wide range of linguistic features out of the box, including part-of-speech tagging, dependency parsing, named entity recognition, and more. These features can be valuable for understanding and extracting meaningful information from text, which is crucial for identifying action items and assignees.
- Pretrained Models: SpaCy offers pre-trained models for various languages, including English. These models are trained on large corpora and can provide a good starting point for your NLP task. 

*On the other hand, LSTM models are commonly used for sequence modeling tasks, while LLMs like GPT (Generative Pre-trained Transformer) are powerful for text generation and language understanding. Both require huge datasets for training as the more the datasets more trained and the better the accuracy currently our datasets are not so huge ( **less than 10 MB**) which results in low accuracy from the models. And I've also less experience with these models as they require large computational power for training models which requires lots of time. Therefore using Spacy for developing the NLP model best and I have also experienced working with Spacy and its pre-trained models.*

### Citations:
- Dataset link: Hugging Face's https://huggingface.co/datasets/knkarthick/AMI/tree/main
- User Experience and Summarization Function [Optional] for NLP Model and Creativity for end-to-end project website, my last project: https://github.com/AmeenUrRehman/NotesBrainy


### Limitations of the current approach
- Currently, the model is not able to fetch the text columns from the CSV file directly for the generation of the NLP model to return extracted action items and assignees. Users have to copy from the text column and paste it into the text area for the training of the NLP model. 
- The accuracy of the model is quite low as using the basic Python library Spacy and it's a pre-trained model which does not understand highly complex contextual dependencies.
- While the code checks for proper nouns as potential assignees, it may not cover all possible assignee references in the text. Can use Entity recognition in the future for more accuracy.
- Extracting action items solely based on nouns and verbs may result in false positives or noisy extractions. Incorporating additional rules or heuristics specific to the domain or task can help filter out irrelevant information and improve the precision of the extracted action items.

**Note**: For User Experience, I've provided the display directly to the html page so the user can easily copy or paste it into the text area for further processing.

### Loom Video
**Link:** https://www.loom.com/share/68044d7fa373491a8ab17c500bba58ad?sid=70fc9b10-49c3-4248-ab02-801d8eebe766