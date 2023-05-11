import openai
import yaml
import torch
# from yaml.loader import SafeLoader
# with open('/Users/debal/Desktop/ml-engineering-intern-task/data/env.yml','r') as f:
#     data = yaml.load(f, Loader=SafeLoader)
# openai.organization = data["OPEN_API_ORG"]
# openai.api_key = data["OPENAI_API_KEY"]

def get_completion(prompt, model="gpt-3.5-turbo",temperature=0.0):
    """
    This is a helper function to use the openai api for chat completion
    to complete certain text based tasks, and get output in the desired format.
    params:
        prompt: the prompt to be used for describing the task
        type: str
        model: the model to be used for completion
        type: str
        temperature: the degree of randomness of the model's output
        type: float
    """
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']


def cos_sim(a, b):
    """
    Computes the cosine similarity cos_sim(a[i], b[j]) for all i and j.
    :return: Matrix with res[i][j]  = cos_sim(a[i], b[j])
    """
    if not isinstance(a, torch.Tensor):
        a = torch.tensor(a)

    if not isinstance(b, torch.Tensor):
        b = torch.tensor(b)

    if len(a.shape) == 1:
        a = a.unsqueeze(0)

    if len(b.shape) == 1:
        b = b.unsqueeze(0)

    a_norm = torch.nn.functional.normalize(a, p=2, dim=1)
    b_norm = torch.nn.functional.normalize(b, p=2, dim=1)
    return torch.mm(a_norm, b_norm.transpose(0, 1))