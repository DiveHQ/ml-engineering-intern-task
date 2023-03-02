## ![Dive Logo](https://user-images.githubusercontent.com/424487/219708981-f0416526-ba48-4b01-b5b3-c0eb73362718.png) Dive

### Company information

<!--- Use this section to share information about your company such as founding information, mission statement, product description, product success, etc.--->

### Why participate in an Octernship with Dive

<!--- Use this section to appeal to students. Consider sharing information about recent projects, the technology stack, the type of mentorship students can expect, listing future employment opportunities, etc. --->

### Octernship role description: Machine Learning Engineering Intern

<!--- Use this section to describe the role in as much detail as necessary. Please include the GitHub Classroom assignment submission date, length of the Octernship, and the monthly stipend --->

### Recommended qualifications

<!--- Use this section to describe what skills a student might need to complete the problem statement on GitHub Classroom --->

### Eligibility

To participate, you must be:
* 18 years or older

## Assignment

# Identify action items from meeting transcripts

### Task instructions

There are two objectives:

1. [Training data generation / gathering](#1-training-data)
2. [Develop NLP model for Transcript to Action items pipeline](#2-develop-nlp-model)

#### 1. Training Data

Any successful ML implementation depends on data on which models can be trained and tested against
- Generate or gather publicly available meeting transcript data to be used in the next phase of model development
- Use the following CSV format to generate data:
```csv
start_time,end_time,speaker,text
“HH:MM:SS”,“HH:MM:SS”,“Alice”,“Hello everyone!”
"01:00:00","01:01:20","Bob","Today we are going to discuss about overall product metrics"
"12:01:34","12:01:50","Tay","Awesome, thanks for informing about that!"
```

- Document the entire process of generating the training and tradeoffs taken in `APPROACH.md`

#### 2. Develop NLP Model

From meeting transcripts, identify action items (tasks to be done) that were identified during the course of the meeting.

**Input: transcript text as generated in 1st objective**
```csv
“10:00:00”, “10:01:50”, “Bob“, “... Alice, can you take the UX bug? ...”
“12:25:00”, “12:25:30”, “Alice”, ”... We need to plan for offsite next month ...”
```

**Output: action items**
  - format: `{"text": ..., "assignee": "Name or UNKNOWN"}`
  - for the above example:
```json
{"text": "UX bug", "assignee": "Alice"}
{"text": "plan for offsite next month", "assignee": "UNKNOWN"}
```

(optional) Stretch goal: Keep the timestamp of when the action item was detected in the transcript
  - format: `"ts": "HH:MM:SS"`
  - for the above example:
```json
{"text": "UX bug", "assignee": "Alice", "ts": "10:00:00"}
{"text": "plan for offsite next month", "assignee": "UNKNOWN", "ts": "12:25:00"}
```


### Task Expectations
- Evaluation criteria: 50% of Approach Document, 50% of functional code and demo video
- Creativity in sourcing training data
- Ability to develop end-to-end PoC
- Using a pre-trained SOTA is acceptable, along with appropriate citation
- Code Quality - remove any unnecessary code, avoid large functions
- Good commit history - we won’t accept a repo with a single giant commit 🙅‍♀️


### Task submission

2. Making changes on the auto generated `feedback` branch to complete the task
3. Using the auto generated **Feedback Pull Request** for review and submission
4. Using GitHub Discussions to ask any relevant questions regarding the project
5. Final submission Checklist:
- [ ] `APPROACH.md` Document
  - note all the approaches considered
  - document any assumptions made and why
  - what did you pick first and why (it’s okay to say - because I am familiar with the process)
  - what did you stop considering and why e.g. (didn’t use LSTM due to low accuracy)
  - citation: links to any code, article or paper referred to
  - what are the limitations of the current approach
- [ ] `SUBMISSION.md` file in the repo, with steps to
  - setup the codebase (including installing dependencies)
  - run the pipeline, which generates a transcript and prints the action items (one per line)
- [ ] [loom.com](<http://loom.com>) video 📹 recording of the demo, where you:
  - generate a new transcript file
  - feed it to the model to extract a list of action items
