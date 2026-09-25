import os
from dotenv import load_dotenv

load_dotenv()

BUCKET = "ncam-documents"

_supabase_client = None


def get_client():
    global _supabase_client
    if _supabase_client is None:
        from supabase import create_client
        from supabase.lib.client_options import SyncClientOptions
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")
        if not url or not key:
            raise Exception(
                "SUPABASE_URL and SUPABASE_SERVICE_KEY must be "
                "set in your .env file."
            )
        # eu-west-1 can be slow from Nigeria; storage3's 20s default is
        # too short for real PDFs, so give uploads/downloads more room.
        options = SyncClientOptions(
            storage_client_timeout=120,
            postgrest_client_timeout=60,
        )
        _supabase_client = create_client(url, key, options)
    return _supabase_client


def upload_document(
    file_bytes: bytes,
    file_name: str,
    project_id: int,
    category: str
) -> str:
    storage_path = f"project_{project_id}/{category}/{file_name}"
    last_err = None
    for _attempt in range(2):
        try:
            get_client().storage.from_(BUCKET).upload(
                path=storage_path,
                file=file_bytes,
                file_options={
                    "content-type": "application/octet-stream",
                    "upsert": "true",
                }
            )
            return storage_path
        except Exception as e:
            last_err = e
    raise Exception(
        f"Upload failed after 2 attempts (check network / file size): {last_err}"
    )


def get_document_url(storage_path: str) -> str:
    response = get_client().storage.from_(BUCKET).create_signed_url(
        path=storage_path,
        expires_in=3600
    )
    return response.get("signedURL", "")


def list_project_documents(project_id: int) -> list:
    try:
        folder = f"project_{project_id}"
        response = get_client().storage.from_(BUCKET).list(folder)
        return response or []
    except Exception:
        return []


def delete_document(storage_path: str) -> bool:
    try:
        get_client().storage.from_(BUCKET).remove([storage_path])
        return True
    except Exception:
        return False