import json 

def load_agent_config(path): 
    with open (path, "r") as file: 
        config = json.load(file)
    return config