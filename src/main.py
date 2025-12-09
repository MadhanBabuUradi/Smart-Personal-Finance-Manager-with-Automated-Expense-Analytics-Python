import argparse
from pathlib import Path
from src.utils.file_handler import read_expenses_csv, write_csv
from src.utils.data_cleaning import sanitize_categories, ensure_amounts
from src.services.expense_service import ExpenseService
from src.services.analytics_service import AnalyticsService
from src.utils.plotting import save_pie_by_category, save_monthly_trend, save_savings_forecast
from src.services.report_service import PDFReport

def run(input_csv, output_dir):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    df = read_expenses_csv(input_csv)
    df = sanitize_categories(df)
    df = ensure_amounts(df)

    # services
    expense_svc = ExpenseService(df)
    analytics = AnalyticsService(expense_svc.get_transactions())

    # generate charts
    pie = out/'dashboards'/'category_pie.png'
    monthly = out/'dashboards'/'monthly_trend.png'
    savings = out/'dashboards'/'savings_forecast.png'

    save_pie_by_category(df, str(pie))
    save_monthly_trend(df, str(monthly))
    save_savings_forecast(df, str(savings))

    # create pdf report
    pdf = PDFReport(title='Auto Finance Report')
    pdf.add_title('Automated Personal Finance Report')
    pdf.add_paragraph('Summary: This report contains charts generated from your expense data.')
    pdf.add_image(str(pie))
    pdf.add_image(str(monthly))
    pdf.add_image(str(savings))
    pdf_path = out/'reports'/'monthly_report.pdf'
    pdf.save(str(pdf_path))
    print('Done. Outputs saved to', out)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='data/sample_expenses.csv')
    parser.add_argument('--output', default='outputs')
    args = parser.parse_args()
    run(args.input, args.output)
