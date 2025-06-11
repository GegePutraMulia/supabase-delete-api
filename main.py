from fastapi import FastAPI
import requests
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = FastAPI()

# Supabase config (ambil dari environment variable)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_BUCKET_NAME = os.getenv("SUPABASE_BUCKET")

# Inisialisasi Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.delete("/hapus-user/{user_id}")
def hapus_user(user_id: str):
    # Ambil data user dari Firestore
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        return {"error": "User tidak ditemukan"}

    user_data = user_doc.to_dict()
    foto_url = user_data.get("foto_anggota", "")

    # Ekstrak path dari URL Supabase
    if "object/public/" in foto_url:
        path = foto_url.split("object/public/")[1]
    else:
        path = None

    # Hapus file dari Supabase jika ada path
    if path:
        headers = {
            "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
            "Content-Type": "application/json"
        }
        delete_url = f"{SUPABASE_URL}/storage/v1/object/remove"
        response = requests.post(delete_url, headers=headers, json={
            "bucketName": SUPABASE_BUCKET,
            "paths": [path]
        })

        if response.status_code != 200:
            return {
                "error": "Gagal hapus file dari Supabase",
                "supabase_response": response.text
            }

    # Hapus dokumen Firestore
    user_ref.delete()

    return {
        "status": "sukses",
        "user_id": user_id,
        "foto_path": path
    }
