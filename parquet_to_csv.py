import pandas as pd

try:
    with open("swabd") as file:
        pd.read_parquet("swabd").to_csv("swab_status.csv")
    print("Success! File name is swab_status.csv")
except FileNotFoundError:
    print("Please ensure that the file exists!")
