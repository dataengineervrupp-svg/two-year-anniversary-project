# print('hello world')
# from pathlib import Path
# PROJECT_ROOT = Path(__file__).resolve().parent
# SPECS_DIR = PROJECT_ROOT / "specs"
# print("Project root:", PROJECT_ROOT)
# print("Specs dir:", SPECS_DIR)

# for path in sorted(SPECS_DIR.glob("*.md")):
#     print(path)

# PROMPTS_DIR = PROJECT_ROOT / "ai_builder" / "prompts"
# print("Prompts dir:", PROMPTS_DIR)
# for path in sorted(PROMPTS_DIR.glob("*.md")):
#     print(path)

from pathlib import Path
import pandas as pd
def load_dating_log_dataframe() -> pd.DataFrame:
    """
    Load the dating log CSV into a pandas DataFrame.
    Expects:
        dating_log_connie.csv in project root
    Returns:
        pandas DataFrame with parsed dates
    """

    project_root = Path(__file__).resolve().parent
    csv_path = project_root / "dating_log_connie.csv"
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Could not find CSV file at: {csv_path}"
        )
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["Date_Date"]).dt.date
    df.drop(columns=['Date', 'Description'], inplace=True)
    df.rename(columns={'Date_Date':'date_str'}, inplace=True)
    return df

df = load_dating_log_dataframe()
print(df['Category'].value_counts())