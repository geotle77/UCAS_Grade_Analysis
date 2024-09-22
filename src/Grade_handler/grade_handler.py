from Grade_handler.grade2gpa import Grade2gpa
import os
import json
import csv
import re

BASE_PATH = "./data"
class grade_handler():
    def __init__(self, std: Grade2gpa, grade: str) -> None:
        self.std = std
        self._loadgrade(grade)
        self.terms= set()
        self.skip = False
        self._grade_filter()

    
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
       
    def _get_gpa(self, term: str) -> float:
        total_credit = 0
        total_gpa = 0
        for course in self.grade:
            if course["学期"] == term:
                credit = course["学分"]
                grade = course["成绩"]
                if grade in self.std.transition_dict["Letter Grade System"].keys():
                    gpa = self.std.transition_dict["Letter Grade System"][grade]
                elif grade in self.std.transition_dict["Five-point Scale"].keys():
                    gpa = self.std.transition_dict["Five-point Scale"][grade]
                else:
                    gpa = self._percentage_gpa(course)
                total_credit += credit
                total_gpa += credit * gpa
        return total_gpa / total_credit
    
    def _percentage_gpa(self, course) -> float:
        transition_table = self.std.pec_trans_table
        for bound in transition_table.keys():
            if course["成绩"] <=59:
                return 0
            if course["成绩"] >= bound[0] and course["成绩"] <= bound[1]:
                return transition_table[bound]
    
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
    def get_gpa(self):
        self.mege_ungraded()
        for term in self.terms:
            print(f"the gpa of term {term} is {self._get_gpa(term)}")