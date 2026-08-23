import os
import json
import pymupdf as fitz  # PyMuPDF (import as pymupdf; fitz alias kept for compatibility)
import docx
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_text_from_file(
    file_bytes: bytes,
    file_name: str
) -> str:
    """
    Extracts plain text from PDF or DOCX files.
    """
    ext = file_name.lower().split(".")[-1]

    if ext == "pdf":
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            return text[:8000]
        except Exception as e:
            raise Exception(f"PDF extraction failed: {e}")

    elif ext in ["docx", "doc"]:
        try:
            import io
            document = docx.Document(io.BytesIO(file_bytes))
            text = "\n".join([p.text for p in document.paragraphs])
            return text[:8000]
        except Exception as e:
            raise Exception(f"DOCX extraction failed: {e}")

    else:
        return ""


def extract_research_details(
    file_bytes: bytes,
    file_name: str
) -> dict:
    """
    Uses Groq to extract structured research details
    from document text.
    Returns a dict of extracted fields.
    """
    raw_text = extract_text_from_file(file_bytes, file_name)

    if not raw_text.strip():
        return {
            "error": "Could not extract text from this file. "
                     "It may be a scanned image or unsupported format."
        }

    system_prompt = """You are a research document analysis assistant for the National Centre for Agricultural Mechanization (NCAM) in Nigeria.

You will be given text extracted from a research document — this could be a research paper, technical report, project proposal, or evaluation report.

Your job is to extract the following fields from the text and return them as a valid JSON object. If a field cannot be found, return null for that field.

Return ONLY a valid JSON object with these exact keys:
{
    "title": "Full title of the research or paper",
    "lead_researcher": "Name of the lead/first author or lead researcher",
    "supervisor": "Name of the supervisor or principal investigator if mentioned",
    "keywords": "Comma-separated keywords",
    "summary": "A 3-5 sentence summary of what the research is about",
    "objectives": "The stated objectives or aims of the research",
    "findings": "Key findings or results if available",
    "funding_source": "Funding body or source if mentioned",
    "journal_name": "Journal or conference name if this is a published paper",
    "publication_date": "Publication or completion date in YYYY-MM-DD format if found, otherwise null",
    "start_date": "Research start date in YYYY-MM-DD format if found, otherwise null",
    "end_date": "Research end date in YYYY-MM-DD format if found, otherwise null",
    "research_type": "One of: Experimental, Applied, Adaptive, Survey, Review, Development, Evaluation, Other",
    "machine_built": true or false based on whether a machine or prototype was developed
}

Return ONLY the JSON object. No preamble, no explanation, no markdown formatting."""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Extract research details from this document:\n\n{raw_text}"
                }
            ],
            temperature=0.1,
            max_tokens=1000
        )

        raw_response = response.choices[0].message.content.strip()
        raw_response = raw_response.replace(
            "```json", ""
        ).replace("```", "").strip()
        extracted = json.loads(raw_response)
        extracted["raw_extraction"] = raw_response
        return extracted

    except json.JSONDecodeError:
        return {
            "error": "AI returned an unexpected format. "
                     "Please fill the fields manually.",
            "raw_extraction": raw_response
        }
    except Exception as e:
        return {"error": str(e)}