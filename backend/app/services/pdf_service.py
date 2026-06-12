from pypdf import PdfReader


def extract_pages_from_pdf(file_path):

    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages):

        text = page.extract_text()

        pages.append({
            "page": page_number + 1,
            "text": text
        })

    return pages