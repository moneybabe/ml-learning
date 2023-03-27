import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def read_csv():
    df = pd.read_csv("data.csv", names=["Date", "CPI"], index_col="Date", parse_dates=True)
    # df.index = pd.to_datetime(df.index)
    df["CPI"] = df["CPI"].str.rstrip("%").astype(float)
    X = np.array(range(0, len(df.index))).reshape(-1,1)
    y = df["CPI"]
    df["X"] = X

    return X, y, df

def df_cov_var_lin_reg(df):
    cov = df.cov().loc["X","CPI"]
    var = df.var().loc["X"]
    slope = cov / var
    intercept = df.mean().loc["CPI"] - slope*df.mean().loc["X"]

    return slope, intercept

def loop_lin_reg(X, y):
    sum = 0
    for i in y:
        sum += i
    y_mean = sum / len(y)

    sum = 0
    for i in X:
        sum += i[0] 
        X_mean = sum / len(X)

    cov = 0
    for i in range(len(y)):
        cov += (X[i, 0] - X_mean) * (y[i] - y_mean)

    var = 0
    for i in range(len(X)):
        var += (X[i, 0] - X_mean) ** 2

    slope = cov / var
    intercept = y_mean - (slope * X_mean)

    return slope, intercept

def main():
    X, y, df = read_csv()
    lr = LinearRegression()
    lr.fit(X, y)
    df["LR CPI"] = lr.predict(X)

    plt.figure(1)
    plt.plot(df["CPI"], label="CPI")
    plt.plot(df["LR CPI"], label="LR CPI")
    
    plt.xlabel("Year")
    plt.ylabel("CPI Value (%)")
    plt.axhline(0, color="k", linestyle="dashed", linewidth=0.5)
    plt.title("US CPI vs Year")
    plt.margins(x=0)
    plt.legend()

    plt.show() 

if __name__ == "__main__":
    main()


"""if wanted to split into train and test set"""
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=87)
# lr = LinearRegression()
# lr.fit(X_train.reshape(-1,1), y_train)
# y_predict = lr.predict(X_test.reshape(-1,1))