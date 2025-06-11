from fastapi import FastAPI
import requests

app = FastAPI()

SUPABASE_PROJECT_ID = "https://juigrfuhshdlsbphvvqx.supabase.co"  # Ganti dengan ID project Supabase kamu
SUPABASE_SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1aWdyZnVoc2hkbHNicGh2dnF4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NzU4NDU2OSwiZXhwIjoyMDYzMTYwNTY5fQ.o2BcOHorJnkcDuuOJLFhkaA6bXeylDOgtXw-1p--Cic"  # Ganti dengan service_role key kamu
SUPABASE_BUCKET = "foto-profil"

@app.delete("/delete-foto/{filename}")
def delete_foto(filename: str):
    url = f"https://juigrfuhshdlsbphvvqx.supabase.co/storage/v1/object/remove"
    headers = {
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "bucketName": SUPABASE_BUCKET,
        "paths": [f"anggota/{filename}"]
    }

    response = requests.post(url, json=body, headers=headers)
    if response.status_code == 200:
        return {"status": "success", "detail": f"anggota/{filename} deleted"}
    else:
        return {"status": "error", "detail": response.json()}
