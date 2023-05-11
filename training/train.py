import pandas as pd
import json
from datasets import Dataset
import torch
from torch.utils.data import DataLoader
from torch.optim import AdamW
from transformers import (AutoTokenizer,
                         BartForConditionalGeneration, 
                         T5ForConditionalGeneration, 
                         BloomForCausalLM,
                         get_scheduler)
import wandb
from tqdm.auto import tqdm
import sys
sys.path.append('../')
from utils import *
from fuzzywuzzy import fuzz

def evaluate(action_true,action_pred):
    
    if not action_true and not action_pred:
        return (1,0,0,0)
    elif action_true and not action_pred:
        return (0,0,1,0)
    elif not action_true and action_pred:
        return (0,0,0,1)
    else:
    
        embed_1 = [get_embedding(item['text']) for item in action_true]
        embed_2 = [get_embedding(item['text']) for item in action_pred]

        scores = cos_sim(embed_1,embed_2)
        top_idx = torch.argmax(scores,dim=1)
        exact_match = 0
        wrong_assignee = 0
        not_found = 0
        extra_generated = len(action_pred) - len(action_true) if len(action_pred) > len(action_true) else 0
        for i,idx in enumerate(top_idx):
            if scores[i][idx] > 0.85:
                if fuzz.partial_ratio(action_true[i]['assignee'],action_pred[idx]['assignee']) >= 100:
                    exact_match += 1
                else:
                    wrong_assignee += 1
            else:
                not_found += 1
        metrics = [exact_match,wrong_assignee,not_found]
        metrics = [x/len(action_true) for x in metrics] + [extra_generated]
        return tuple(metrics)

def prepare_dataset(dialogue_path:str,labels_path:str,tokenizer:AutoTokenizer):
    df_train = pd.read_csv(dialogue_path)
    df_train['id'] = df_train['id'].astype(str)

    # dataset = []
    with open(labels_path,'r') as f:
        labels = json.load(f)

    
    
    dataset = []
    dialogue_len = 0
    max_len = 0
    for i,item in enumerate(labels):
        temp = {}
        dialogues = df_train[df_train.id == item['id']][['speaker','text']].values
        dialogues = [': '.join(x) for x in dialogues]
        dialogue_str = '\n'.join(dialogues)
        if 't5' in model_name:
            dialogue_str = 'Find Action Items from the following chat:\n' + dialogue_str
        if 'bloom' in model_name:
            res = 'Action Item:\n'+item['label']
            res = res.replace('\n','[SEP]')
            dialogue_str = dialogue_str + '[SEP][SEP]' + res
            temp['conversation'] = dialogue_str
            temp['action_item'] = res
        else:
            temp['conversation'] = dialogue_str
            temp['action_item'] = 'Action Item:\n'+item['label']
            temp['action_item'] = temp['action_item'].replace('\n','[SEP]')
        if len(tokenizer.encode(dialogue_str)) > 512:
            continue
        else:
            dialogue_len += len(tokenizer.encode(dialogue_str))
            if len(tokenizer.encode(dialogue_str.split("[SEP][SEP]")[0])) > max_len:
                max_len = len(tokenizer.encode(dialogue_str))
            dataset.append(temp)
    
    return dataset, max_len

def process_output(out_ids):
    action_items = tokenizer.batch_decode(out_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
    action_items = [x.split('[SEP]')[1:] for x in action_items]
    final_preds = []
    for item in action_items:
        temp =  []
        if item:
            for action in item:
                # print(action)
                try:
                    temp.append({'text':action.split('||')[0],'assignee':action.split('||')[1]})
                except:
                    continue
        final_preds.append(temp)
    return final_preds


if __name__ == '__main__':

    model_name = "philschmid/bart-large-cnn-samsum"    

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    if 't5' in model_name:
        model = T5ForConditionalGeneration.from_pretrained(model_name)
    elif 'bloom' in model_name:
        model = BloomForCausalLM.from_pretrained(model_name)
    else:
        model = BartForConditionalGeneration.from_pretrained(model_name)

    tokenizer.add_tokens(['[SEP]'])
    model.resize_token_embeddings(len(tokenizer))

    data, max_len = prepare_dataset('../data/datasets/dialogue.csv','../data/datasets/labels.json',tokenizer)

    def preprocess_function(examples):
        model_inputs = tokenizer(examples['conversation'],max_length=512, padding="max_length")
        
        # Setup the tokenizer for targets
        with tokenizer.as_target_tokenizer():
            labels = tokenizer(examples["action_item"], max_length=256, padding="max_length")

        model_inputs["labels"] = labels["input_ids"]
        if "bloom" in model_name:
            inp_text = [text.split("[SEP][SEP]")[0] for text in examples['conversation']]
            generation_tokens = tokenizer(inp_text,max_length=max_len, padding="max_length")
            model_inputs["genrate_input_ids"] = generation_tokens["input_ids"]
        return model_inputs
        
    dataset = Dataset.from_list(data)
    dataset_dict = dataset.train_test_split(test_size=0.2,seed = 2) 

    tokenized_datasets = dataset_dict.map(preprocess_function, batched=True)

    tokenized_datasets = tokenized_datasets.remove_columns(['conversation','action_item'])

    tokenized_datasets.set_format("torch")
    batch_size = 2 if "bloom" in model_name else 8 
    train_dataloader = DataLoader(tokenized_datasets['train'], shuffle=True, batch_size=batch_size)
    eval_dataloader = DataLoader(tokenized_datasets['test'], batch_size=batch_size)

    optimizer = AdamW(model.parameters(), lr=5e-5)
    num_epochs = 10
    num_training_steps = num_epochs * len(train_dataloader)
    lr_scheduler = get_scheduler(
        name="linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=num_training_steps
    )

    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    model.to(device)

    config = {
    "epochs" : num_epochs,
    "train_batch_size" : 2,
    "model_architecture" : "bloom-560m",
    "pretraining_dataset" : "N/A",   
        }
    run = wandb.init(
    project="action-item-extractor",
    notes="architecture-comparisson",
    config=config
    )

    

    progress_bar = tqdm(range(num_training_steps))

    model.train()
    for epoch in range(num_epochs):
        total_loss = 0
        for batch in train_dataloader:
            if "bloom" in model_name:
                batch = {k: v.to(device) for k, v in batch.items() if k in ['input_ids','attention_mask']}
                outputs = model(input_ids=batch["input_ids"],
                                attention_mask = batch["attention_mask"],
                                labels = batch["input_ids"])
            else:
                batch = {k: v.to(device) for k, v in batch.items()}
                outputs = model(**batch)
            loss = outputs.loss
            total_loss += loss.item()
            loss.backward()
            
            optimizer.step()
            lr_scheduler.step()
            optimizer.zero_grad()
            progress_bar.update(1)
            torch.cuda.empty_cache()
            # break
        with torch.no_grad():
            eval_loss = 0
            exact_match = 0
            wrong_assignee = 0
            not_found = 0
            extra_generated = 0
            for batch in eval_dataloader:
                batch = {k: v.to(device) for k, v in batch.items()}
                if "bloom" in model_name:
                    outputs = model(input_ids=batch["input_ids"],
                                    attention_mask = batch["attention_mask"],
                                    labels = batch["input_ids"])
                else:
                    outputs = model(**batch)
                eval_loss += outputs.loss.item()
                
                true_vals = process_output(batch["labels"])
                if "bloom" in model_name:
                    pred_ids = model.generate(batch["genrate_input_ids"],max_length=512)
                else:
                    pred_ids = model.generate(batch["input_ids"],max_length=256)
                pred_vals = process_output(pred_ids)
                metrics = [evaluate(true_vals[i],pred_vals[i]) for i in range(batch['input_ids'].shape[0])]
                metrics = [sum(i) for i in zip(*metrics)]
                exact_match += metrics[0]
                wrong_assignee += metrics[1]
                not_found += metrics[2]
                extra_generated += metrics[3]
        log_dict = {
        "train_loss" : total_loss/len(dataset_dict['train']),
        "eval_loss" :  eval_loss/len(eval_dataloader),
        "exact_match" : exact_match/(len(dataset_dict['test'])),
        "wrong_assignee" : wrong_assignee/(len(dataset_dict['test'])),
        "not_found" : not_found/(len(dataset_dict['test'])),
        'extra_generated' : extra_generated/(len(dataset_dict['test']))    
        }
        print(log_dict)
        wandb.log(log_dict)
    
    model.save_pretrained('../bart-finetuned-action-items')
    tokenizer.save_pretrained('../bart-finetuned-action-items')