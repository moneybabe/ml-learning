import pandas as pd

df = pd.read_csv("data.csv", names=["Date", "CPI"])
print(df.head(10))