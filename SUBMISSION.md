Certainly! Here's a template for proper documentation for the project:

# ML MODEL


## Video Of Running Model
https://www.loom.com/share/f6cb0537486a4e6bb703ef42fb1061a1?sid=a7b98369-0d14-45fb-ade5-11c4f055702b


## Description
The project aims to extract action items from meeting transcripts using a pre-trained BERT model for text classification. It identifies sentences or phrases that represent tasks to be done and assigns them to the appropriate assignee. The output is a list of action items with their corresponding assignees.

## Prerequisites
- Python (version 3.11.1 or higher)
- Libraries:
  - torch 
  - transformers

## Installation
1. Install Python:
   - Download and install Python from the official Python website (python.org).

2. Install the required libraries:
   - Open a terminal or command prompt.
   - Run the following commands:
     ```
     pip install torch
     pip install transformers
```
## To run the code in a Python virtual environment, you can follow these steps:

1. Set up a virtual environment: Open a terminal or command prompt and navigate to your project directory. Create a new virtual environment by running the following command:
   ```
   python -m venv myenv
   ```

2. Activate the virtual environment: Activate the virtual environment by running the appropriate command based on your operating system:
   - For Windows:
     ```
     myenv\Scripts\activate
     ```
   - For macOS/Linux:
     ```
     source myenv/bin/activate
     ```

3. Install the necessary libraries: Make sure you have the required libraries installed. In this case, you need to have Python installed along with the `pandas` library for data manipulation and the `torch` and `transformers` libraries for BERT model usage. You can install them using `pip` by running the following command:
   ```
   pip install pandas torch transformers
   ```

4. Set up the code: Copy the provided code into a Python file, such as `meeting_transcript.py`, using a text editor or an integrated development environment (IDE) like Visual Studio Code or PyCharm.

   ```
   python meeting_transcript.py
   ```

7. View the output: The code will process the meeting transcripts and extract the action items. The extracted action items will be printed on the console or terminal as dictionaries in the format: `{"text": ..., "assignee": ...}`. Review the printed output to see the identified action items.

Ensure that you have the necessary permissions and access to the required data or files mentioned in the code. Modify the code as needed to fit your specific use case or requirements.

Remember to deactivate the virtual environment once you're done by running the command `deactivate` in the terminal or command prompt.



## Usage
1. Clone or download the project repository.

2. Prepare the Meeting Transcripts:
   - Open the project folder.
   - Locate the `transcripts.txt` file.
   - Update the file with the meeting transcripts in the following format:
     ```
     "start_time","end_time","speaker","text"
     "00:00:00","00:00:15","Alice","Good afternoon, everyone!"
     "00:00:15","00:00:40","Bob","Good afternoon, Alice. How was your weekend?"
     ...
     ```
   - Save the file with the updated meeting transcripts.

3. Run the Code:
   - Open a terminal or command prompt.
   - Navigate to the project folder.
   - Execute the following command:
     ```
     python ml_model_1.py
     ```

4. Review the Results:
   - The extracted action items will be displayed in the console or output window.
   - Each action item will be shown in the format: `{"text": ..., "assignee": ...}`.
   - Optionally, the timestamp of when the action item was detected can be included.

## Customization and Further Steps
- Customize the code to meet specific requirements, such as modifying the text classification model or integrating with other tools.
- Explore enhancements, such as fine-tuning the model for improved accuracy or integrating with project management tools.
- Refer to the code comments for guidance on customizing or extending the functionality.


## Troubleshooting
- If encountering any errors, ensure that all prerequisites are properly installed.
- Verify that the meeting transcripts are correctly formatted in the `gathered-data.csv` file.

## License
This project is licensed under the MIT License

## Acknowledgments
We would like to acknowledge the following resources and projects that contributed to the development of this project:

BERT - Pre-trained model for text classification.
Transformers - Library for natural language processing tasks.


## References
BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
The Illustrated Transformer
Hugging Face Transformers Documentation
