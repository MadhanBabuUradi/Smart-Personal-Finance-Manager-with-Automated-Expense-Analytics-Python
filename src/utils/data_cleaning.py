def sanitize_categories(df):
    # simple cleaning: fillna and title case categories
    df['category'] = df['category'].fillna('Uncategorized').astype(str).str.strip().str.title()
    return df

def ensure_amounts(df):
    df['amount'] = df['amount'].astype(float)
    return df
