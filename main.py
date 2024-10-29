from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from PyPDF2 import PdfReader
from datetime import datetime
import os
from time import sleep


app = FastAPI()

templates = Jinja2Templates(directory="templates")


async def validate_file(file):
    # if file isn't an pdf then raise exception
    if file[0:4] != b"%PDF":
        raise Exception("File is not a PDF")

    # get file name
    fname = f"file-{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"

    # save file in temporary directory
    with open(fname, "wb") as f:
        f.write(file)

    # read the pdf file to validate
    reader = PdfReader(fname)
    if len(reader.pages) == 0:
        raise Exception("File is empty")

    if reader.pages[0].extract_text() == "":
        raise Exception("File is empty")

    if reader.pages[0].extract_text().strip() == "":
        raise Exception("File is empty")

    # check if it's password protected
    if reader.is_encrypted:
        # delete the file if exists
        if fname in os.listdir():
            os.remove(fname)
        raise Exception("File is password protected")

    # delete the file if exists
    if fname in os.listdir():
        os.remove(fname)

    return {"message": "File validated successfully"}


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.post("/validate-file")
async def validate_file_api(file: bytes = File(...)):
    try:
        return await validate_file(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "File uploaded successfully"}


@app.post("/upload")
async def upload_file(file: UploadFile):
    try:
        # again validate file
        await validate_file(file.file.read())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # save it permanently
    # create directory if it doesn't exist
    if not os.path.exists("files"):
        os.mkdir("files")
    fpath = f'files/{file.filename.replace(" ", "_").replace(".pdf", "")}-{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf'
    with open(fpath, "wb") as f:
        f.write(file.file.read())

    return {"file_size": os.path.getsize(fpath)}
