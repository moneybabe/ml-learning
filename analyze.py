import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

df = pd.read_csv("data.csv", names=["Date", "CPI"], index_col="Date", parse_dates=True)
# df.index = pd.to_datetime(df.index)
df["CPI"] = df["CPI"].str.rstrip("%").astype(float)

X = np.array(range(0, len(df.index)))
y = df["CPI"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=87)
lr = LinearRegression()
lr.fit(X_train.reshape(-1,1), y_train)
y_predict = lr.predict(X_test.reshape(-1,1))

plt.scatter(X_test, y_test)
plt.plot(X_test, y_predict)
plt.show()




# plt.figure(1)
# plt.xlabel("Year")
# plt.ylabel("CPI Value (%)")
# plt.axhline(0, color="k", linestyle="dashed", linewidth=0.5)
# plt.title("US CPI vs Year")
# plt.margins(x=0)
# plt.plot(df)
# plt.show() 
