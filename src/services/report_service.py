from fpdf import FPDF
from pathlib import Path

class PDFReport:
    def __init__(self, title='Monthly Report'):
        self.title = title
        self.pdf = FPDF()

    def add_title(self, text):
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(0, 10, text, ln=True, align='C')

    def add_paragraph(self, text):
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(0, 8, text)

    def add_image(self, img_path, w=160):
        Path(img_path).parent.mkdir(parents=True, exist_ok=True)
        if Path(img_path).exists():
            self.pdf.image(img_path, w=w)

    def save(self, out_path):
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        self.pdf.output(out_path)
