from pypdf import PdfReader

pdf = PdfReader("book.pdf")
text = ""

for page in pdf.pages:
    text += page.extract_text()

with open("data.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("PDF converted successfully!")