import os
import pandas as pd
import json
import re

class Grade2gpa():
    def __init__(self,transition_std:str="Grade2gpa.json") -> None:
        self.std = transition_std
        if not os.path.exists(self.std):
            raise FileNotFoundError(f"文件 {self.std} 不存在")
        with open(self.std,"r") as f:
            self.transition_dict = json.load(f)
        self._extract_bounds()
    
    def __str__(self) -> str:
        return f"Grade2gpa transition standard: {self.std}"
    
    def show(self) -> None:
        formatted_out = json.dumps(self.transition_dict,indent=4,ensure_ascii=False)
        print(formatted_out)
    
    def _extract_bounds(self):
        self.pecentage_bounds = [key for key in self.transition_dict["Percentage System"].keys()]
        self.pec_trans_table = {}
        for bound in self.pecentage_bounds:
            if bound == "补考合格":
                self.pec_trans_table["补考合格"] = self.transition_dict["Percentage System"]["补考合格"]
            else:  
                match = re.match(r"(\d+)(?:-(\d+))?",bound)
                if match:
                    lower_bound = int(match.group(1))
                    upper_bound = int(match.group(2)) if match.group(2) else lower_bound
                    self.pec_trans_table[(lower_bound,upper_bound)] = self.transition_dict["Percentage System"][bound]  
                else:
                    raise ValueError(f"百分制成绩区间 {bound} 格式错误")
          
