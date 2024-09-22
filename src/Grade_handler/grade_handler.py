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
        self.term_course={}
        self._grade_filter()

    
    def _loadgrade(self, grade: str) -> None:
        with open(grade, "r") as f:
            self.grade = list(csv.DictReader(f))
    
    def _grade_filter(self):
        self.ungraded = []
        filtered_grade = []
        for course in self.grade:
            if course["评估状态"] == "未参加评估":
                print(f"the course {course['课程名称']} in {course['学期']}has not been evaluated")
                self.ungraded.append(course)
            elif course["成绩"] == "合格" or course["成绩"] == "不合格" or course["成绩"] == "W":
                print(f"the course {course['课程名称']} in {course['学期']} has been removed")
            else:
                filtered_grade.append(course)
            self.terms.add(course["学期"])
        self.grade = filtered_grade
        print(f"do you want to skip the unevaluated courses? (y/n)")
        choice = input() 
        if choice == "y":
            self.skip = True
       
    def _get_gpa(self, term: list) -> float:
        total_credit = 0
        total_gpa = 0
        for course in term:
            credit = float(course["学分"])
            total_credit += credit
            gpa = self._percentage_gpa(course)
            total_gpa += gpa * credit
        return total_gpa / total_credit
    
    def _percentage_gpa(self, course) -> float:
        transition_table = self.std.pec_trans_table
        if course["成绩"] == "补考合格":
            return transition_table["补考合格"]
        grade = float(course["成绩"])
        for bound in transition_table.keys():
            if grade >= bound[0] and grade <= bound[1]:
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
        for course in self.grade:
            for term in self.terms:
                if course["学期"] == term:
                    self.term_course.setdefault(term,[]).append(course)

        for term_courses in self.term_course.values():
            gpa = self._get_gpa(term_courses)
            print(f"the gpa of term {term_courses[0]['学期']} is {gpa}")