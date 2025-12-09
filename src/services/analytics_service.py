import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

class AnalyticsService:
    def __init__(self, df):
        self.df = df.copy()

    def spending_by_category(self):
        return self.df.groupby('category')['amount'].sum().sort_values(ascending=False)

    def monthly_trends(self):
        df2 = self.df.copy()
        df2['month'] = df2['date'].dt.to_period('M').dt.to_timestamp()
        return df2.groupby('month')['amount'].sum().sort_index()

    def top_categories(self, n=5):
        return self.spending_by_category().head(n)

    def overspending_alerts(self, threshold):
        # simplistic: months where monthly spend > threshold
        monthly = self.monthly_trends()
        return monthly[monthly > threshold]

    def savings_prediction(self):
        # simple linear regression of savings over months (income - non-income)
        df2 = self.df.copy()
        df2['month'] = df2['date'].dt.to_period('M').dt.to_timestamp()
        monthly = df2.groupby(['month','category'])['amount'].sum().unstack(fill_value=0)
        income = monthly.get('Income', pd.Series(0, index=monthly.index))
        expenses = monthly.sum(axis=1) - income
        savings = (income - expenses).fillna(0)
        X = np.arange(len(savings)).reshape(-1,1)
        y = savings.values
        if len(X) < 2:
            return pd.Series(savings, index=monthly.index)
        model = LinearRegression().fit(X, y)
        pred = model.predict(X)
        return pd.Series(pred, index=monthly.index)
