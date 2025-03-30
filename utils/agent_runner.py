import threading 
from runner_agent import run_agent_from_file


class AgentController: 
    def __init__(self): 
        self.running_threads = {}
    
    def start_agent(self, agent_name, config_path):
        if agent_name in self.running_threads: 
            print(f"[INFO] Agent {agent_name} is already running.")
            return False
        
        thread = threading.Thread(target=run_agent_from_file, args=(config_path, ), daemon=True)
        thread.start()
        self.running_threads[agent_name] = thread
        print(f"[INFO] Agent {agent_name} started.")
        return True
    
    def stop_agent(self, agent_name):
        if agent_name in self.running_threads: 
            del self.running_threads[agent_name]
            print(f"[INFO] Agent {agent_name} stopped.")
            return True
        else:
            print(f"[INFO] Agent {agent_name} is not running.")
            return False
    
    def is_running(self, agent_name):
        return agent_name in self.running_threads
