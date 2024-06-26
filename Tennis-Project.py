import zipfile
import pandas as pd
import os

# مسیر فایل zip اصلی و مسیر استخراج
zip_path = r'C:\Users\Fatemeh\Downloads\data.zip'
extract_path = r'C:\Users\Fatemeh\Desktop\Tennis-Project'
output_csv_path = r'C:\Users\Fatemeh\Desktop\Tennis-Project\CSV_Files'

# اطمینان از وجود پوشه مقصد
os.makedirs(extract_path, exist_ok=True)
os.makedirs(output_csv_path, exist_ok=True)

# استخراج فایل zip اصلی
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# لیست فایل‌های استخراج شده
extracted_files = os.listdir(extract_path)
print("Extracted files from main zip:")
for file in extracted_files:
    print(file)

# جداول مورد انتظار بر اساس اسکیمای ارائه شده
expected_tables = {
    'MatchEventInfo': None,
    'PeriodInfo': None,
    'MatchVotesInfo': None,
    'MatchTournamentInfo': None,
    'MatchSeasonInfo': None,
    'MatchRoundInfo': None,
    'MatchVenueInfo': None,
    'MatchHomeTeamInfo': None,
    'MatchAwayTeamInfo': None,
    'MatchHomeScoreInfo': None,
    'MatchAwayScoreInfo': None,
    'MatchTimeInfo': None,
    'GameInfo': None,
    'OddsInfo': None,
    'PowerInfo': None
}

# استخراج و بارگذاری داده‌های zip داخلی
for file in extracted_files:
    if file.endswith('.zip'):
        inner_zip_path = os.path.join(extract_path, file)
        inner_extract_path = os.path.join(extract_path, file.replace('.zip', ''))
        os.makedirs(inner_extract_path, exist_ok=True)
        
        try:
            with zipfile.ZipFile(inner_zip_path, 'r') as inner_zip_ref:
                try:
                    inner_zip_ref.extractall(inner_extract_path)
                    print(f"Extracted {inner_zip_path} to {inner_extract_path}")
                except zipfile.BadZipFile:
                    print(f"Error: {inner_zip_path} is a bad zip file.")
                    continue
                except EOFError:
                    print(f"Error: {inner_zip_path} is incomplete or corrupted.")
                    continue
        except Exception as e:
            print(f"Error opening {inner_zip_path}: {e}")
            continue

        # لیست فایل‌های استخراج شده از زیپ داخلی
        inner_extracted_files = os.listdir(inner_extract_path)
        print(f"Extracted files from {inner_zip_path}:")
        for inner_file in inner_extracted_files:
            print(inner_file)

        for root, _, inner_files in os.walk(inner_extract_path):
            for inner_file in inner_files:
                if inner_file.endswith('.csv'):
                    try:
                        file_path = os.path.join(root, inner_file)
                        df = pd.read_csv(file_path)
                        table_name = inner_file.replace('.csv', '')
                        if table_name in expected_tables:
                            expected_tables[table_name] = df
                            print(f"Loaded {inner_file} from {file_path}")
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

# ایجاد دیتافریم‌های خالی برای جداولی که پیدا نشدند
for table_name in expected_tables:
    if expected_tables[table_name] is None:
        print(f"DataFrame for {table_name} not found, creating empty DataFrame.")
        expected_tables[table_name] = pd.DataFrame()

# ذخیره تمامی دیتافریم‌ها به فایل‌های CSV
for table_name, df in expected_tables.items():
    output_file_path = os.path.join(output_csv_path, f"{table_name}.csv")
    df.to_csv(output_file_path, index=False)
    print(f"Saved DataFrame for {table_name} to {output_file_path}")

# چاپ مسیر فایل‌های CSV
print("\nAll CSV file paths:")
for root, _, files in os.walk(output_csv_path):
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(root, file)
            print(f"File path: {file_path}")