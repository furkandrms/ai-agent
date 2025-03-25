class BaseTask: 

    def __init__(self, config):
        self.config = config
    
    def execute(self, personality):
        raise NotImplementedError("Subclasses must implement execute method")
    