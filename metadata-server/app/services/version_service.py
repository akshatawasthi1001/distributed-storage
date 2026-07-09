import os
import shutil

from fastapi import HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.models.file_model import File as FileModel
from app.models.file_version_model import FileVersion

STORAGE_DIR = "storage"


def replace_file(
    file_id: str,
    file,
    db: Session,
    current_user
):

    file_record = (
        db.query(FileModel)
        .filter(
            FileModel.id == file_id,
            FileModel.owner_id == current_user.id
        )
        .first()
    )

    if not file_record:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    new_version = file_record.current_version + 1

    _, extension = os.path.splitext(file.filename)

    new_filename = (
        f"{file_record.id}_v{new_version}{extension}"
    )

    new_path = os.path.join(
        STORAGE_DIR,
        new_filename
    )

    with open(new_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    new_size = os.path.getsize(new_path)

    file_record.filename = file.filename
    file_record.storage_path = new_path
    file_record.size = new_size
    file_record.current_version = new_version

    version_record = FileVersion(
        file_id=file_record.id,
        version=new_version,
        storage_path=new_path,
        size=new_size
    )

    db.add(version_record)
    db.commit()
    db.refresh(file_record)

    return {
        "message": "File updated successfully",
        "file_id": str(file_record.id),
        "filename": file_record.filename,
        "current_version": file_record.current_version,
        "size": file_record.size
    }


def get_versions(
    file_id: str,
    db: Session,
    current_user
):

    file = (
        db.query(FileModel)
        .filter(
            FileModel.id == file_id,
            FileModel.owner_id == current_user.id
        )
        .first()
    )

    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    versions = (
        db.query(FileVersion)
        .filter(FileVersion.file_id == file_id)
        .order_by(FileVersion.version.asc())
        .all()
    )

    return [
        {
            "version": v.version,
            "size": v.size,
            "storage_path": v.storage_path,
            "created_at": v.created_at
        }
        for v in versions
    ]


def download_version(
    file_id: str,
    version: int,
    db: Session,
    current_user
):

    file = (
        db.query(FileModel)
        .filter(
            FileModel.id == file_id,
            FileModel.owner_id == current_user.id
        )
        .first()
    )

    if not file:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    version_record = (
        db.query(FileVersion)
        .filter(
            FileVersion.file_id == file_id,
            FileVersion.version == version
        )
        .first()
    )

    if not version_record:
        raise HTTPException(
            status_code=404,
            detail="Version not found"
        )

    return FileResponse(
        path=version_record.storage_path,
        filename=os.path.basename(version_record.storage_path),
        media_type="application/octet-stream"
    )