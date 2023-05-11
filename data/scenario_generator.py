import yaml
from yaml.loader import SafeLoader
import pandas as pd
from tqdm.auto import tqdm
import re
import random
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

    # Generate a list of names
    prompt_names = "Generate 100 names of people" # Generating random names to be use dfor dialogue generation
    names = get_completion(prompt_names,temperature=0.4)
    names = names.split('\n')
    names = [re.sub(r'\d+\.\s+', '', name) for name in names]

    # Generate scenario for give scene
    dialogue_id = 0
    dataset = []
    labels = []
    remaining = []
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
            dataset.append([inp,', '.join(participants),turns])
    
    df_scenario = pd.DataFrame(dataset,columns=['scenario','participants','turns'])
    df_scenario.to_csv('datasets/scenario.csv',index=False)
