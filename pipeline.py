import pandas as pd
import yaml
from yaml.loader import SafeLoader
import random
from transformers import AutoTokenizer, BartForConditionalGeneration
import json
from data.utils import get_completion

with open('data/datagen_vars.yml','r',encoding='UTF-8') as f:
        data = yaml.load(f, Loader=SafeLoader)


# ======================================= RealTime Dialogue generation Code =======================================
df = pd.read_csv('data/datasets/inference_scenario.csv')

tokenizer = AutoTokenizer.from_pretrained("Debal/action-item-generator")

model = BartForConditionalGeneration.from_pretrained("Debal/action-item-generator")

exp = data['example'].split('Action Items:\n')[0]
example = random.choice(list(df.values))
prompt_dialogue = f"""
{exp}

Scenario: {example[0]}
Participants : {example[1]}
Turns: {example[2]}
"""

response = get_completion(prompt_dialogue)

dialogue = response.split('\n')
dialogue_list = [diag.split('||')[-2:] for diag in dialogue]
dialogue_list = [":".join(x) for x in dialogue_list]
inp = '\n'.join(dialogue_list)

# ======================================= Static Dialogue Fetch =======================================
# with open('data/datasets/inference_data.json','r') as f:
#     data = json.load(f)

# inp = random.choice(data)

print("Input\n", inp)
exit()
inputs = tokenizer([inp],return_tensors='pt')
summary_ids = model.generate(inputs["input_ids"],max_length=256)
action_items = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
action_list = action_items.split('\n')[1:]
action_list = [{'text':x.split('||')[0],'assignee':x.split('||')[1]} for x in action_list]

for item in action_list:
    print(item)