import pandas as pd
import os

BASE_FILE_PATH = r"f:/CODES/Python/UCAS_Grade_Analysis/src"

def read_data(file_name: str) -> None:
    file_path = os.path.normpath(os.path.join(BASE_FILE_PATH, "data", file_name))
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件 {file_path} 不存在")
    df = pd.read_excel(file_path)
    csv_file = file_path.replace(".xlsx", ".csv")
    df.to_csv(csv_file, index=False)
    print(f"文件已成功转换并保存为 {csv_file}")

if __name__ == "__main__":
    print(f"当前工作目录: {os.getcwd()}")
    read_data("Grade.xlsx")