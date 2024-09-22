from Grade_handler.grade2gpa import Grade2gpa
import os
import json
import csv

BASE_PATH = "./data"
class grade_handler():
    def __init__(self, std: Grade2gpa, grade: str) -> None:
        self.std = std
        self._loadgrade(grade)
        self.terms= set()
        self.skip = False

    
    def _loadgrade(self, grade: str) -> None:
        with open(grade, "r") as f:
            self.grade = list(csv.DictReader(f))
    
    def _grade_filter(self):
        self.ungraded = []
        for course in self.grade:
            if course["评估状态"] == "未参加评估":
                print(f"the course {course['课程名称']} in {course['学期']}has not been evaluated")
                self.ungraded.append(course)
            self.terms.add(course["学期"])
        print(f"do you want to skip the unevaluated courses? (y/n)")
        choice = input() 
        if choice == "y":
            self.skip = True
        for course in self.grade:
            if course["成绩"] == "合格"|"不合格":
                self.grade.remove(course)
                print(f"the course {course['课程名称']} in {course['学期']} has been removed")
       
    
    def mege_ungraded(self):
        if not self.skip:
            for course in self.grade:
                for ug_course in self.ungraded:
                    if course["课程名称"] == ug_course["课程名称"]:
                        print(f"please input the grade of the course {course['课程名称']} in {course['学期']}")
                        while True:
                            grade = int(input())
                            if grade <= 100 and grade >= 0 or grade in self.std.transition_dict["Letter Grade System"].keys() or grade in self.std.transition_dict["Five-point Scale"].keys():  
                                course["成绩"] = grade
                                break
                
        


        

            
