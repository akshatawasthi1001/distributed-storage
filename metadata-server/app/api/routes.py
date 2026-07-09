import os
import shutil

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
    Query
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.file_model import File as FileModel
from app.models.file_version_model import FileVersion
from app.services.upload_service import upload_new_file
from app.core.dependencies import get_current_user
from app.services.file_service import (
    download_file,
    get_file_metadata,
    search_files,
    delete_file,
    list_files
)
from app.services.version_service import (
    replace_file,
    get_versions,
    download_version
)
router = APIRouter()

STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)


# ===========================
# Upload File
# ===========================

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return upload_new_file(
    file,
    db,
    current_user
)

# ===========================
# List Files
# ===========================

@router.get("/files")
def list_all_files(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return list_files(
        page,
        limit,
        db,
        current_user
    )

# ===========================
# Search Files
# ===========================

@router.get("/files/search")
def search(
    filename: str = Query(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return search_files(filename, db, current_user)

# ===========================
# Download Latest Version
# ===========================

@router.get("/download/{file_id}")
def download(
    file_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return download_file(file_id, db, current_user)


# ===========================
# Delete File
# ===========================

@router.delete("/files/{file_id}")
def delete(
    file_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return delete_file(file_id, db, current_user)

# ===========================
# Replace File (Create New Version)
# ===========================

@router.put("/files/{file_id}")
async def replace(
    file_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return replace_file(
        file_id,
        file,
        db,
        current_user
    )
# ===========================
# Version History
# ===========================

@router.get("/files/{file_id}/versions")
def versions(
    file_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_versions(
        file_id,
        db,
        current_user
    )
# ===========================
# Download Specific Version
# ===========================

@router.get("/files/{file_id}/versions/{version}/download")
def version_download(
    file_id: str,
    version: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return download_version(
        file_id,
        version,
        db,
        current_user
    )

# ===========================
# Get File Metadata
# ===========================

@router.get("/files/{file_id}")
def file_metadata(
    file_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_file_metadata(file_id, db, current_user)