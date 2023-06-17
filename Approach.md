##Approaches Considered

Rule-based Approach: Initially, a rule-based approach was considered where specific patterns or keywords 
related to action items were extracted from the meeting transcripts. Regular expressions or keyword matching 
techniques could be used for this approach.

Named Entity Recognition (NER): Another approach considered was to utilize Named Entity Recognition techniques
to identify action items. NER models could be trained to recognize specific entities related to tasks or actions.

Machine Learning (ML) Approach: The ML approach involved training a model on labeled data where the task was to 
classify sentences or phrases as action items or non-action items. Various ML algorithms such as Naive Bayes, 
Support Vector Machines (SVM), or Random Forests could be explored.


##Assumptions Made

Assumed English Language: The current approach assumes that the meeting transcripts are in the English language.

Assumed Presence of Action Items: It is assumed that the meeting transcripts contain sentences or phrases explicitly 
mentioning action items or tasks to be done


##Chosen Approach
The chosen approach for identifying action items from meeting transcripts is the Machine Learning (ML) Approach. 
This decision was made because of the flexibility and potential accuracy that ML models can offer in classifying 
sentences as action items or non-action items. Additionally, ML models can be trained on labeled data, allowing 
for iterative improvement and fine-tuning.

##Limitations of the Current Approach

Language Dependency: The current approach is limited to meeting transcripts in the English language. 
It may not perform well with transcripts in other languages without appropriate language-specific training.

Generalization to Different Domains: The ML model's performance may vary across different domains or industries.
It may require domain-specific training data or fine-tuning to achieve optimal results in specific contexts.

Accuracy and False Positives: The current approach may have limitations in accurately identifying action items 
and may generate false positives or miss certain action items depending on the complexity and variability of the meeting transcripts.
