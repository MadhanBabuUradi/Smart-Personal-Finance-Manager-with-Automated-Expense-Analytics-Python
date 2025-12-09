import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

sns.set(style='whitegrid', rc={'figure.figsize':(8,5)})

def save_pie_by_category(df, out_path):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    series = df.groupby('category')['amount'].sum().sort_values(ascending=False)
    plt.figure()
    series.plot.pie(autopct='%1.1f%%')
    plt.ylabel('')
    plt.title('Spending by Category')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def save_monthly_trend(df, out_path):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    df2 = df.copy()
    df2['month'] = df2['date'].dt.to_period('M').dt.to_timestamp()
    series = df2.groupby('month')['amount'].sum()
    plt.figure()
    sns.barplot(x=series.index.strftime('%Y-%m'), y=series.values)
    plt.xticks(rotation=45)
    plt.ylabel('Amount')
    plt.title('Monthly Expenses')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def save_savings_forecast(df, out_path):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    # naive forecast: cumulative income - expenses trend (simple)
    df2 = df.copy()
    df2['month'] = df2['date'].dt.to_period('M').dt.to_timestamp()
    monthly = df2.groupby(['month','category'])['amount'].sum().unstack(fill_value=0)
    # assume 'Income' category exists
    income = monthly.get('Income', pd.Series(0, index=monthly.index))
    expenses = monthly.sum(axis=1) - income
    savings = income - expenses
    plt.figure()
    plt.plot(monthly.index.strftime('%Y-%m'), savings.cumsum(), marker='o')
    plt.xticks(rotation=45)
    plt.title('Savings Forecast (Cumulative)')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
