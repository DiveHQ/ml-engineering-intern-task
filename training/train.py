import pandas as pd
import json
from datasets import Dataset
import torch
from torch.utils.data import DataLoader
from torch.optim import AdamW
from transformers import AutoTokenizer, BartForConditionalGeneration, get_scheduler

def prepare_dataset(dialogue_path:str,labels_path:str,tokenizer:AutoTokenizer):
    df_train = pd.read_csv(dialogue_path)
    df_train['id'] = df_train['id'].astype(str)

    # dataset = []
    with open(labels_path,'r') as f:
        labels = json.load(f)

    end = tokenizer.special_tokens_map['eos_token']
    idx = 0
    dataset = []
    dialogue_len = 0
    for item in enumerate(labels):
        temp = {}
        dialogues = df_train[df_train.id == item['id']][['speaker','text']].values
        dialogues = [': '.join(x) for x in dialogues]
        dialogue_str = '\n'.join(dialogues)
        temp['conversation'] = dialogue_str + end
        temp['action_item'] = 'Action Item:\n'+item['label'] + end 
        if len(tokenizer.encode(dialogue_str)) > 512:
            continue
        else:
            dialogue_len += len(tokenizer.encode(dialogue_str))    
            dataset.append(temp)
    
    return dataset


def preprocess_function(examples):
    model_inputs = tokenizer(examples['conversation'],max_length=512, padding="max_length")

    # Setup the tokenizer for targets
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(examples["action_item"], max_length=256, padding="max_length")

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs



if __name__ == '__main__':

    model_name = "philschmid/bart-large-cnn-samsum"    

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model = BartForConditionalGeneration.from_pretrained(model_name)

    data = prepare_dataset('../data/datasets/dialogue.csv','../data/datasets/labels.json',tokenizer)

        
    dataset = Dataset.from_list(data)
    dataset_dict = dataset.train_test_split(test_size=0.2,seed = 2) 

    tokenized_datasets = dataset_dict.map(preprocess_function, batched=True)

    tokenized_datasets = tokenized_datasets.remove_columns(['conversation','action_item'])

    tokenized_datasets.set_format("torch")
    train_dataloader = DataLoader(tokenized_datasets['train'], shuffle=True, batch_size=8)
    eval_dataloader = DataLoader(tokenized_datasets['test'], batch_size=8)

    optimizer = AdamW(model.parameters(), lr=5e-5)
    num_epochs = 10
    num_training_steps = num_epochs * len(train_dataloader)
    lr_scheduler = get_scheduler(
        name="linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=num_training_steps
    )

    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    model.to(device)

    from tqdm.auto import tqdm

    progress_bar = tqdm(range(num_training_steps))

    model.train()
    for epoch in range(num_epochs):
        total_loss = 0
        for batch in train_dataloader:
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
        print(f'Epoch {epoch}','Train Loss :-',total_loss/len(train_dataloader))

    model.save_pretrained('../bart-finetuned-action-items')
    tokenizer.save_pretrained('../bart-finetuned-action-items')