import re
from fastapi import UploadFile, HTTPException, status
from pypdf import PdfReader
import io

from service.analyze_content_service import generate_auto_reply

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "text/plain",
}

ALLOWED_EXTENSIONS = {".pdf", ".txt"}

VERB_SUFFIXES = (
    "ar", "er", "ir",
    "ando", "endo", "indo",
    "ente", "ado", "ido",
    "ou", "ei", "am",
    "ava", "avam",
    "ará", "erá", "irá",
    "aria", "iria", "eria",
    "iriam", "arão", "ito",
    "ido", "ino", "irmo",
)

def read_txt(content: bytes) -> str:
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo TXT não está em UTF-8."
        )

def read_pdf(content: bytes) -> str:
    try:
        pdf = PdfReader(io.BytesIO(content))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo PDF inválido."
        )

    extracted_text = []

    for page in pdf.pages:
        text = page.extract_text()
        if text:
            extracted_text.append(text)

    full_text = "\n".join(extracted_text).strip()

    if not full_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível extrair texto do PDF."
        )

    return full_text

def classify_productivity_by_suffix(text: str):
    words = re.findall(r"\b\w+\b", text.lower())

    matches = {
        word
        for word in words
        if any(word.endswith(suffix) for suffix in VERB_SUFFIXES)
    }

    return "produtivo" if len(matches) >= 2 else "improdutivo"


async def read_uploaded_file(file: UploadFile):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas arquivos PDF ou TXT são permitidos."
        )

    filename = (file.filename or "").lower()
    if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Extensão de arquivo inválida. Use .pdf ou .txt."
        )

    content = await file.read()


    if file.content_type == "text/plain":
        text = read_txt(content)
    else:
        text = read_pdf(content)

    is_productive = classify_productivity_by_suffix(text)

    if(is_productive == "produtivo"):
        auto_reply = generate_auto_reply(text)
    else:
        auto_reply =  "Olá, agradecemos seu contato. \n Vamos analisar a solicitação e retornaremos em breve."

    return {
        "file_content": text,
        "productivity": is_productive,
        "suggestion_reply": auto_reply,
    }
