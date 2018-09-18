from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from pandas import read_csv
from sklearn.model_selection import train_test_split
import pandas

data = read_csv("D:/vgsales.csv", index_col=0)
pandas.set_option('display.max_columns', None)
y = data.Global_Sales
X = data.drop('Global_Sales', axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)


regr = linear_model.LinearRegression()

regr.fit(X_train, y_train)

# Make predictions using the testing set
y_pred = regr.predict(X_test)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(y_test, y_pred))
# Explained variance score: 1 is perfect prediction
print('Variance: %.2f' % r2_score(y_test, y_pred))