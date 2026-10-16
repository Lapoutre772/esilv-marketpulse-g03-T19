from pathlib import Path
import csv

DATA_DIR = Path("data/sample")


def get_first_close():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        prices= list(csv.DictReader(file))    
        print(float(prices[0]["close"]))

def get_last_close():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        prices= list(csv.DictReader(file))    
        print(float(prices[len(prices)-1]["close"]))

prices = get_first_close()
last_price= get_last_close()

