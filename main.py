from fastapi import FastAPI
import requests
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Supabase config
SUPABASE_URL = os.getenv("https://juigrfuhshdlsbphvvqx.supabase.co")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1aWdyZnVoc2hkbHNicGh2dnF4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NzU4NDU2OSwiZXhwIjoyMDYzMTYwNTY5fQ.o2BcOHorJnkcDuuOJLFhkaA6bXeylDOgtXw-1p--Cic")
SUPABASE_BUCKET = os.getenv("foto-profil")

# Firebase init
cred = credentials.Certificate("serviceAccountKey.json")  # download dari Firebase
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.delete("/hapus-user/{user_id}")
def hapus_user(user_id: str):
    # 1. Ambil data user dari Firestore
    user_ref = db.collection("users").document(user_id)
    user_data = user_ref.get().to_dict()

    if not user_data:
        return {"error": "User tidak ditemukan"}

    foto_url = user_data.get("foto_anggota", "")
    
    # 2. Ambil path dari URL
    if "object/public/" in foto_url:
        path = foto_url.split("object/public/")[1]
    else:
        path = None

    # 3. Hapus foto di Supabase
    if path:
        headers = {
            "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            f"{SUPABASE_URL}/storage/v1/object/remove",
            headers=headers,
            json={"bucketName": SUPABASE_BUCKET, "paths": [path]}
        )
        if response.status_code != 200:
            return {"error": "Gagal hapus foto dari Supabase", "detail": response.text}
    
    # 4. Hapus dokumen Firestore
    user_ref.delete()

    return {"status": "sukses", "user_id": user_id, "foto_path": path}
