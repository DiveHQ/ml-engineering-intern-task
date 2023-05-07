import yaml
from yaml.loader import SafeLoader
import pandas as pd
from tqdm.auto import tqdm
import re
import random
import json
from utils import get_completion


if __name__ == '__main__': 
    with open('datagen_vars.yml','r',encoding='UTF-8') as f:
        data = yaml.load(f, Loader=SafeLoader)

    # Generate a list of names
    prompt_names = "Generate 100 names of people" # Generating random names to be use dfor dialogue generation
    names = get_completion(prompt_names,temperature=0.0)
    names = names.split('\n')
    names = [re.sub(r'\d+\.\s+', '', name) for name in names]

    # Generate scenario for give scene
    dialogue_id = 0
    dataset = []
    labels = []
    for scene in data['scene_list']:
        
        prompt_scenario = f"""
Generate 30 Scenarios for which a group of people would meet in a {scene}.
Keep it short
"""
        scenarios = get_completion(prompt_scenario)
        scenarios = scenarios.split('\n')
        scenarios = [re.sub(r'\d+\.\s+', '', scenario) for scenario in scenarios]
        print(scene)
        for scenario in tqdm(scenarios):
            inp = f'{scenario},{scene}'
            num_names = random.randint(2,5)
            participants = random.sample(names,num_names)
            turns = random.randint(3,6)*num_names
            prompt_dialogue = f"""
{data['example']}

Scenario: {inp}
Participants : {', '.join(participants)}
Turns: {turns}
"""
            response = get_completion(prompt_dialogue)
            dialogue, action_items = response.split('\nAction Items:\n')
            dialogue = dialogue.split('\n')
            dialogue_list = [[dialogue_id]+diag.split('||') for diag in dialogue]
            action_items = action_items.split('\n')
            lab = {
                'id' : dialogue_id,
                'label' : action_items
            }
            labels.append(lab)
            dataset.extend(dialogue_list)

    df_dialogue = pd.DataFrame(dataset,columns=['id','start_time','end_time','speaker','text'])
    df_dialogue.to_csv('dialogue.csv',index=False)

    with open('labels.json','w') as f:
        json.dump(labels,f)
                



    #Generate data for given scenario with randomly picked names and randomly found turns