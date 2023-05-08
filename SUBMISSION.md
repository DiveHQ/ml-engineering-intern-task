# Setting up the Enviornment

## Prerequisites
First you need to have conda installed on your machine. If not installed follow the following steps

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh 
conda create --name dive python=3.10
conda activate dive
```
## Installing Dependencies
After creating the enviornment, execute the following command
```
pip install -r requirements.txt
```

## Creating env.yml file
One needs to create a `yml` file for OPENAI APA credentials which would look something like this
```
OPENAI_API_KEY : [API-TOKEN]
OPEN_API_ORG : [ORG-ID]
```
## Running inference

To get the model for running inference you can eithre fetch it from huggingface hub from [here](https://huggingface.co/Debal/action-item-generator)
or one can train the model by doing the following steps:
```
cd training
python train.py
``` 
The above commands will train and save a model checkpoint at `bart-finetuned-action-items/`

To run Inference you need run
```
python pipeline.py
```
If one does not have the api keys he can comment out the chatgpt dialogue generation code and replace it by the following snippet:
```
with open('data/datasets/inference_data.json','r') as f:
    data = json.load(f)

inp = random.choice(data)    
```