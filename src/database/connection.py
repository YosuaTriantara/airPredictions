"""
connection.py
Koneksi ke database (Supabase Postgres) yang dipakai oleh layer `src`
(API/serving) untuk MEMBACA data yang sudah di-ingest oleh `databases/`.

Pakai env var yang SAMA persis dengan yang dipakai `databases/scripts/db.py`
(DATABASE_URL), karena keduanya menunjuk ke satu project Supabase yang sama:

    databases/  -> menulis (ingest OpenAQ -> stations, air_quality_measurements)
    src/        -> membaca (serving prediksi lewat API) + menulis predictions/model_logs
"""

import os
import logging
from contextlib import contextmanager

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "sslmode": os.getenv("DB_SSLMODE", "require"),
}


@contextmanager
def get_connection():
    """Context manager: buka koneksi, commit/rollback otomatis, lalu tutup."""
    if DATABASE_URL:
        conn = psycopg2.connect(DATABASE_URL)
    else:
        conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@contextmanager
def get_cursor(dict_cursor=True):
    """Context manager: langsung dapat cursor siap pakai (dict by default)."""
    with get_connection() as conn:
        cursor_factory = psycopg2.extras.RealDictCursor if dict_cursor else None
        cur = conn.cursor(cursor_factory=cursor_factory)
        try:
            yield cur
        finally:
            cur.close()
