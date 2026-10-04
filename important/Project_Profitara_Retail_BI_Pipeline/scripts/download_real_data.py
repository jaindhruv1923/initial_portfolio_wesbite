import os
import sys
import zipfile
import requests
import io
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "real")
os.makedirs(DATA_DIR, exist_ok=True)

CSV_OUTPUT_PATH = os.path.join(DATA_DIR, "online_retail_II.csv")

# Known primary and mirror URLs for UCI Online Retail II (2009-2011) or UCI Online Retail
URLS = [
    # UCI direct zip
    "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip",
    # UCI single year zip as fallback if multi-year 502 fails
    "https://archive.ics.uci.edu/static/public/352/online+retail.zip",
    # Reliable GitHub mirror of clean Online Retail II / Online Retail CSV
    "https://raw.githubusercontent.com/datagy/data/main/online_retail_II.csv",
    "https://raw.githubusercontent.com/datasets/online-retail-dataset/master/data/online_retail.csv"
]

def download_and_extract():
    if os.path.exists(CSV_OUTPUT_PATH) and os.path.getsize(CSV_OUTPUT_PATH) > 1000000:
        print(f"Dataset already exists at: {CSV_OUTPUT_PATH} ({os.path.getsize(CSV_OUTPUT_PATH):,} bytes)")
        return CSV_OUTPUT_PATH

    print("Attempting to download real retail dataset...")
    success = False
    downloaded_file = None

    for url in URLS:
        try:
            print(f"Trying: {url} ...")
            resp = requests.get(url, stream=True, timeout=60)
            if resp.status_code == 200:
                content = resp.content
                print(f"Downloaded {len(content):,} bytes from {url}")

                if url.endswith(".zip"):
                    with zipfile.ZipFile(io.BytesIO(content)) as z:
                        namelist = z.namelist()
                        print(f"Zip contents: {namelist}")
                        for fname in namelist:
                            if fname.endswith(".xlsx"):
                                excel_path = os.path.join(DATA_DIR, fname)
                                z.extract(fname, DATA_DIR)
                                print(f"Extracted Excel file: {excel_path}. Converting to CSV...")
                                # Load both sheets if Online Retail II has 2 sheets
                                xl = pd.ExcelFile(excel_path)
                                sheet_dfs = []
                                for sheet in xl.sheet_names:
                                    print(f"  Reading sheet: {sheet}")
                                    sheet_dfs.append(pd.read_excel(xl, sheet_name=sheet))
                                combined = pd.concat(sheet_dfs, ignore_index=True)
                                combined.to_csv(CSV_OUTPUT_PATH, index=False)
                                print(f"Saved combined CSV: {CSV_OUTPUT_PATH} with {len(combined):,} rows")
                                success = True
                                break
                            elif fname.endswith(".csv"):
                                z.extract(fname, DATA_DIR)
                                extracted_csv = os.path.join(DATA_DIR, fname)
                                if extracted_csv != CSV_OUTPUT_PATH:
                                    os.replace(extracted_csv, CSV_OUTPUT_PATH)
                                success = True
                                break
                elif url.endswith(".csv"):
                    with open(CSV_OUTPUT_PATH, "wb") as f:
                        f.write(content)
                    success = True
                    break
                
                if success:
                    break
        except Exception as e:
            print(f"Failed from {url}: {e}")

    if not success or not os.path.exists(CSV_OUTPUT_PATH):
        print("ERROR: Automatic download of public dataset failed.")
        print("Please manually download UCI Online Retail II from:")
        print("  https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip")
        print(f"And place the extracted file or converted CSV at: {CSV_OUTPUT_PATH}")
        sys.exit(1)

    print(f"Verification: Successfully prepared real dataset at {CSV_OUTPUT_PATH}")
    df_check = pd.read_csv(CSV_OUTPUT_PATH, nrows=5)
    print("Columns:", df_check.columns.tolist())
    print("Head:\n", df_check.head(2))
    return CSV_OUTPUT_PATH

if __name__ == "__main__":
    download_and_extract()
