from fuzzywuzzy import fuzz
import torch
import openai

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

def evaluate(action_true,action_pred):
    
    embed_1 = [get_embedding(item['text']) for item in action_true]
    embed_2 = [get_embedding(item['text']) for item in action_pred]

    scores = cos_sim(embed_1,embed_2)
    top_idx = torch.argmax(scores,dim=1)
    exact_match = 0
    wrong_assignee = 0
    not_found = 0
    extra_generated = len(action_true) - len(action_pred)
    for i,idx in enumerate(top_idx):
        if scores[i][idx] > 0.85:
            if fuzz.partial_ratio(action_true[i]['assignee'],action_pred[idx]['assignee']) == 100:
                exact_match += 1
            else:
                wrong_assignee += 1
        else:
            not_found += 1
    metrics = [exact_match,wrong_assignee,not_found]
    metrics = [x/len(action_true) for x in metrics] [extra_generated]
    return tuple(metrics)

