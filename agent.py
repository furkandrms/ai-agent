class Agent: 
    def __init__(self, name, personality, tasks): 

        self.name = name
        self.personality = personality
        self.tasks = tasks

    def run(self, config): 
        print("Running agent: " + self.name)
        for task in self.tasks: 
            task.execute(self.personality, config=config)
        print(f"[INFO] Agent {self.name} has completed its tasks.")