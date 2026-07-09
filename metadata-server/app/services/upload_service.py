import os
import shutil

from sqlalchemy.orm import Session

from app.models.file_model import File as FileModel
from app.models.file_version_model import FileVersion

STORAGE_DIR = "storage"

os.makedirs(STORAGE_DIR, exist_ok=True)


def upload_new_file(
    file,
    db: Session,
    current_user
):

    file_path = os.path.join(
        STORAGE_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    file_size = os.path.getsize(file_path)

    new_file = FileModel(
        filename=file.filename,
        storage_path=file_path,
        size=file_size,
        current_version=1,
        owner_id=current_user.id
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    version = FileVersion(
        file_id=new_file.id,
        version=1,
        storage_path=file_path,
        size=file_size
    )

    db.add(version)
    db.commit()

    return {
        "file_id": str(new_file.id),
        "filename": new_file.filename,
        "size": new_file.size,
        "saved_at": new_file.storage_path
    }