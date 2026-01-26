import PyPDF2
import os

def read_pdf(path):
    """
    Reads a PDF file and returns its full text as a single string.
    """
    text = ""
    with open(path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def read_pdfs_from_folder(folder_path):
    """
    Reads all PDFs in a folder and returns a list of dictionaries:
    [{"source": filename, "text": text}, ...]
    """
    knowledge = []
    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf"):
            path = os.path.join(folder_path, file)
            print(f"📄 Scanning {file} ...")
            text = read_pdf(path)
            # split text into chunks (paragraphs)
            chunks = text.split("\n\n")
            for chunk in chunks:
                chunk = chunk.strip()
                if len(chunk) > 50:  # ignore very short chunks
                    knowledge.append({
                        "source": file,
                        "text": chunk
                    })
    return knowledge
