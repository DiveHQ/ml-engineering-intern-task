import openai
import yaml
from yaml.loader import SafeLoader
with open('../env.yml','r') as f:
    data = yaml.load(f, Loader=SafeLoader)
openai.organization = data["OPEN_API_ORG"]
openai.api_key = data["OPENAI_API_KEY"]

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