import pandas as pd
import os
from Grade_handler.grade2gpa import Grade2gpa
from Grade_handler.grade_handler import grade_handler

BASE_FILE_PATH = r"src/data"

def read_data(file_name: str) -> None:
    file_path = os.path.join(os.path.join(BASE_FILE_PATH, file_name))
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件 {file_path} 不存在")
    df = pd.read_excel(file_path)
    csv_file = file_path.replace(".xlsx", ".csv")
    df.to_csv(csv_file, index=False)
    print(f"文件已成功转换并保存为 {csv_file}")




if __name__ == "__main__":
    std_file  = os.path.join(os.path.join(BASE_FILE_PATH, "Grade2gpa.json"))
    grade_file = os.path.join(os.path.join(BASE_FILE_PATH, "Grade.csv"))
    transition = Grade2gpa(std_file)
    handler = grade_handler(transition, grade_file)
    transition.show()
    handler.get_gpa()