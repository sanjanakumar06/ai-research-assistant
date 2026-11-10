
import fitz


def extract_pdf_pages(pdf_bytes: bytes) -> list[dict]:
    """
    Extract text from a PDF while preserving page numbers.
    """

    pages = []

    with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
        for page_index, page in enumerate(document):

            text = page.get_text("text")

            pages.append({
                "page_number": page_index + 1,
                "text": text.strip()
            })

    return pages
