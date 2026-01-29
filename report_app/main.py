import os
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

REPORTS_DIR = Path(__file__).parent / "files"
VITE_HOST = os.getenv("APP_VITE_HOST", "localhost")
VITE_PORT = os.getenv("APP_VITE_PORT", "5173")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://{VITE_HOST}:{VITE_PORT}"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReportItem(BaseModel):
    name: str
    size: int
    modified: datetime


@app.get("/reports", response_model=list[ReportItem])
def list_reports():
    if not REPORTS_DIR.exists():
        raise HTTPException(status_code=500, detail="Reports directory does not exist")

    reports: list[ReportItem] = []
    for f in REPORTS_DIR.iterdir():
        if f.is_file():
            stat = f.stat()
            reports.append(
                ReportItem(
                    name=f.name,
                    size=stat.st_size,
                    modified=datetime.fromtimestamp(stat.st_mtime),
                )
            )

    reports.sort(key=lambda r: r.modified, reverse=True)
    return reports


@app.get("/reports/{filename}")
def download_report(filename: str):
    file_path = REPORTS_DIR / filename
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Report not found")

    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type="application/octet-stream",
    )
