from Grade_handler.grade2gpa import Grade2gpa
import os
import json
import csv

BASE_PATH = "./data"
class grade_handler():
    def __init__(self, std: str = "Grade2gpa.json", grade: str = "Grade.csv") -> None:
        self.std = std
        self.transition = self.grade2gpa(std)
        self._loadgrade(grade)
    
    def _loadgrade(self, grade: str) -> None:
        with open(grade, "r") as f:
            self.grade = list(csv.DictReader(f))
    
    def _grade_filter(self):
        for course in self.grade:
            if course["评估状态"] == "未参加评估":
                print(f"the course {course['课程名称']} in {course['学期']}has not been evaluated")
    
    def grade2gpa(self, std: str) -> dict:
        with open(std, "r") as f:
            return json.load(f)
            
