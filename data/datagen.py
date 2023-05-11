import yaml
from yaml.loader import SafeLoader
import pandas as pd
from tqdm.auto import tqdm
import re
import random
import json
import os
from yaml.loader import SafeLoader
import yaml
import openai
import sys
sys.path.append('../')
from utils import get_completion


if __name__ == '__main__': 

    with open('../env.yml','r') as f:
        data = yaml.load(f, Loader=SafeLoader)
    openai.organization = data["OPEN_API_ORG"]
    openai.api_key = data["OPENAI_API_KEY"]

    with open('datagen_vars.yml','r',encoding='UTF-8') as f:
        data = yaml.load(f, Loader=SafeLoader)

    df_scenario = pd.read_csv('datasets/scenario.csv')
    
    
    
    try:
        df_dialogue = pd.read_csv('datasets/dialogue.csv')
    except Exception as e:
        df_dialogue = pd.DataFrame([]) 
    
    try:
        with open('datasets/labels.json','r') as f:
            labels = json.load(f)
    except Exception as e:
        labels = []
    
    try:
        with open('datasets/incorrect.json','r') as f:
            incorrect = json.load(f)
    except Exception as e:
        incorrect = []
    
    if not df_dialogue.empty:
        last_visited_id = max(df_dialogue['id'].unique())
    else:
        last_visited_id = 0
    
    dataset = []  
    # Generating data for given scenario with randomly picked names and randomly found turns  
    for i,row in tqdm(enumerate(df_scenario.iloc[last_visited_id:].values)):

    
            prompt_dialogue = f"""
{data['example']}

Scenario: {row[0]}
Participants : {row[1]}
Turns: {row[2]}
"""
    
            response = get_completion(prompt_dialogue)
            try:
                dialogue, action_items = response.split('\nAction Items:\n')
            except:
                print(response)
                incorrect.append(response)
                continue

            dialogue = dialogue.split('\n')
            dialogue_list = [[i+last_visited_id]+diag.split('||') for diag in dialogue]

            lab = {
                'id' : str(i+last_visited_id),
                'label' : action_items
            }
            dataset.extend(dialogue_list)
            labels.append(lab)
            if (i+1) % 10 ==0: # Saving after every 10 dialogue generation
                df_temp = pd.DataFrame(dataset,columns=['id','start_time','end_time','speaker','text'])
                if not df_dialogue.empty:
                    df_dialogue = pd.concat([df_dialogue,df_temp])
                else:
                    df_dialogue = df_temp
                df_dialogue.to_csv('datasets/dialogue.csv',index=False)    
                dataset = []
                with open('datasets/labels.json','w') as f:
                    json.dump(labels,f)

                if incorrect:
                    with open('datasets/incorrect.json','w') as f:
                        json.dump(incorrect,f)    
                
    
    