import pandas as pd
import os

def load_ticker_list() -> list:
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    csv_path = os.path.join(ROOT_DIR, "config", "tickers.csv")
    df = pd.read_csv(csv_path)
    return df["symbol"].tolist()

tickers = load_ticker_list()
print(tickers)


