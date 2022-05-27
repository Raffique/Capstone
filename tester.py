import pandas as pd

file = "traincut.csv"
report = "report.csv"

file = pd.read_csv(file)
report = pd.read_csv(report)

for i, el in file.iterrows():
    