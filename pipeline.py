import pandas as pd
import yaml
from yaml.loader import SafeLoader
import random
from transformers import AutoTokenizer, BartForConditionalGeneration
import json
from utils import get_completion

tokenizer = AutoTokenizer.from_pretrained("Debal/bart-large-samsum-action-items")

model = BartForConditionalGeneration.from_pretrained("Debal/bart-large-samsum-action-items")



## ======================================= RealTime Dialogue generation Code =======================================
# df = pd.read_csv('data/datasets/inference_scenario.csv')

# with open('data/datagen_vars.yml','r',encoding='UTF-8') as f:
#         data = yaml.load(f, Loader=SafeLoader)


# exp = data['example'].split('Action Items:\n')[0]
# example = random.choice(list(df.values))
# prompt_dialogue = f"""
# {exp}

# Scenario: {example[0]}
# Participants : {example[1]}
# Turns: {example[2]}
# """

# response = get_completion(prompt_dialogue)

# dialogue = response.split('\n')
# dialogue_list = [diag.split('||')[-2:] for diag in dialogue]
# dialogue_list = [":".join(x) for x in dialogue_list]
# inp = '\n'.join(dialogue_list)

## ======================================= Static Dialogue Fetch =======================================
with open('data/datasets/inference_data.json','r') as f:
    data = json.load(f)

inp = random.choice(data)
# response = """
# "10:00:00||10:01:50||John||Good morning everyone, let's start with our daily standup meeting.\n10:02:00||10:03:30||Sarah||I have been working on the transaction module and have completed the integration with the payment gateway. \n10:03:40||10:05:00||David||I have been working on the user authentication module and have found some issues with the password reset functionality. \n10:05:10||10:06:30||John||David can you please create a ticket for this issue and assign it to yourself?\n10:06:40||10:08:00||David||Sure John, I will do that.\n10:08:10||10:09:30||Emily||I have been working on the account balance module and have found some performance issues. \n10:09:40||10:11:00||John||Emily can you please investigate the issue and provide a solution by the end of the day? And Sarah please ghelp Emily if she has any issues.\n10:11:10||10:12:30||Emily||Sure John, I will do that.\n10:12:40||10:14:00||Sarah||I have also found some issues with the transaction history module. \n10:14:10||10:15:30||John||Sure Sarah, I can pick that up? And can someone please create minutes of the meetings.\n"""
# dialogue = response.split('\n')
# dialogue_list = [diag.split('||')[-2:] for diag in dialogue]
# dialogue_list = [":".join(x) for x in dialogue_list]
# inp = '\n'.join(dialogue_list)

print("Input\n", inp)

inputs = tokenizer([inp],return_tensors='pt')
summary_ids = model.generate(inputs["input_ids"],max_length=256)
action_items = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
action_list = action_items.split('[SEP]')[1:]
action_list = [{'text':x.split('||')[0],'assignee':x.split('||')[1]} for x in action_list]

with open('result.json','w') as f:
    json.dump(action_list,f)
for item in action_list:
    print(item)