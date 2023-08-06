from pydantic import BaseModel, EmailStr,validator
from typing import List, IO, Union, Any
from fastapi import UploadFile
import  os
from mimetypes import MimeTypes

class MessageSchema(BaseModel):
    receipients: List[EmailStr]
    attachments: List[Any] = []
    subject: str = ""
    body: str = None
    cc: List[EmailStr] = []
    bcc: List[EmailStr] = []
    charset: str = "utf-8"

    @validator("attachments")
    def validate_file(cls,v):
        temp = []
        for file in v:
            if isinstance(file,str):

                if os.path.isfile(file) and os.access(file, os.R_OK):
                    # mime = magic.Magic(mime=True)
                    mime = MimeTypes()
                    mime_type = mime.guess_type(file)
                    with open(file,mode="rb") as f:
                        u = UploadFile(f.name,f.read(),content_type=mime_type[0])
                        temp.append(u)
                else:
                    raise  ValueError("incorrect file path for attachment or not readable")
            elif isinstance(file,UploadFile):
                temp.append(file)
            else:
                raise  ValueError("attachments field type incorrect, must be UploadFile or path")
        return temp


