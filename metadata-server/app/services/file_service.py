import os

from fastapi import HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.models.file_model import File as FileModel


def list_files(
    page: int,
    limit: int,
    db: Session,
    current_user
):

    offset = (page - 1) * limit

    files = (
        db.query(FileModel)
        .filter(FileModel.owner_id == current_user.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return [
        {
            "id": str(file.id),
            "filename": file.filename,
            "size": file.size,
            "storage_path": file.storage_path
        }
        for file in files
    ]


def search_files(
    filename: str,
    db: Session,
    current_user
):

    files = (
        db.query(FileModel)
        .filter(
            FileModel.owner_id == current_user.id,
            FileModel.filename.ilike(f"%{filename}%")
        )
        .all()
    )

    return [
        {
            "id": str(file.id),
            "filename": file.filename,
            "size": file.size,
            "storage_path": file.storage_path
        }
        for file in files
    ]


def download_file(
    file_id: str,
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

    return FileResponse(
        path=file_record.storage_path,
        filename=file_record.filename,
        media_type="application/octet-stream"
    )


def delete_file(
    file_id: str,
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

    if os.path.exists(file_record.storage_path):
        os.remove(file_record.storage_path)

    db.delete(file_record)
    db.commit()

    return {
        "message": "File deleted successfully",
        "file_id": file_id
    }


def get_file_metadata(
    file_id: str,
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

    return {
        "id": str(file_record.id),
        "filename": file_record.filename,
        "size": file_record.size,
        "storage_path": file_record.storage_path,
        "current_version": file_record.current_version
    }