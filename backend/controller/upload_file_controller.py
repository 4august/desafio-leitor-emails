from fastapi import APIRouter, UploadFile, File

from service.upload_file_service import read_uploaded_file

router = APIRouter()


@router.post("/upload-file/")
async def upload_text_file_controller(
    filePdfTxt: UploadFile = File(...)
):
    return await read_uploaded_file(filePdfTxt)
