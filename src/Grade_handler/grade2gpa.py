import os
import pandas as pd
import json

class Grade2gpa():
    def __init__(self,transition_std:str="Grade2gpa.json") -> None:
        self.std = transition_std
        if not os.path.exists(self.std):
            raise FileNotFoundError(f"文件 {self.std} 不存在")
        with open(self.std,"r") as f:
            self.transition_dict = json.load(f)
    
    def __str__(self) -> str:
        return f"Grade2gpa transition standard: {self.std}"
    
    def show(self) -> None:
        formatted_out = json.dumps(self.transition_dict,indent=4,ensure_ascii=False)
        print(formatted_out)

if __name__ == "__main__":
    transition = grade2gpa()
    transition.show()
