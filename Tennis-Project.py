import zipfile
import pandas as pd
import os

# مسیر فایل zip اصلی و مسیر استخراج
zip_path = r'C:\Users\Fatemeh\Downloads\data.zip'
extract_path = r'C:\Users\Fatemeh\Desktop\Tennis-Project'

# اطمینان از وجود پوشه مقصد
os.makedirs(extract_path, exist_ok=True)

# استخراج فایل zip اصلی
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# لیست فایل‌های استخراج شده
extracted_files = os.listdir(extract_path)

# استخراج و بارگذاری داده‌های zip داخلی
dataframes = {}
for file in extracted_files:
    if file.endswith('.zip'):
        inner_zip_path = os.path.join(extract_path, file)
        inner_extract_path = os.path.join(extract_path, file.replace('.zip', ''))
        os.makedirs(inner_extract_path, exist_ok=True)
        
        try:
            with zipfile.ZipFile(inner_zip_path, 'r') as inner_zip_ref:
                inner_zip_ref.extractall(inner_extract_path)
        except zipfile.BadZipFile:
            print(f"Error: {inner_zip_path} is a bad zip file.")
            continue

        for root, _, inner_files in os.walk(inner_extract_path):
            for inner_file in inner_files:
                if inner_file.endswith('.csv'):
                    try:
                        file_path = os.path.join(root, inner_file)
                        df = pd.read_csv(file_path)
                        dataframes[inner_file] = df
                        print(f"Loaded {inner_file} from {file_path}")
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

# نمایش نمونه‌ای از دیتافریم‌ها
for file, df in dataframes.items():
    print(f"DataFrame from {file}:")
    print(df.head())

# چاپ مسیر فایل‌های CSV
for root, _, files in os.walk(extract_path):
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(root, file)
            print(f"File path: {file_path}")
