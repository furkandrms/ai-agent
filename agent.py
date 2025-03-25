class Agent: 
    def __init__(self, name, personality, tasks): 

        self.name = name
        self.personality = personality
        self.tasks = tasks

    def run(self): 
        print("Running agent: " + self.name)
        for task in self.tasks: 
            task.execute(self.personality)