from typing import Optional, Annotated

from fastapi import FastAPI, UploadFile, File, Form
from pydantic import AnyHttpUrl, UrlConstraints, BaseModel, validator


class TopicGenInputSchema(BaseModel):
    text: Optional[str] = None
    ImgUrl: Annotated[
        Optional[AnyHttpUrl],
        UrlConstraints(allowed_schemes=["https"]),
        Form(description=(
            "Image url only accepts https scheme. It mutually excludes Img"
        ))
    ] = None
    Img: Annotated[
        Optional[UploadFile],
        # image file must be end with .jpg, .png, .jpeg
        File(
            description="Image file. It mutually excludes ImgUrl",
            regex=r"^.+\.(jpg|png|jpeg)$"
        )
    ] = None

    # imgurl and img are mutually exclusive
    @validator("ImgUrl", "Img", always=True)
    def check_imgurl_img_mutually_exclusive(cls, v, values):
        if v is not None and values['Img'] is not None:
            raise ValueError("ImgUrl and Img are mutually exclusive")
        return v

    # text must exist if imgurl or img are None
    @validator('text', always=True)
    def check_text_exists_if_imgurl_img_none(cls, v, values):
        if v is None and values['Img'] is None and values['ImgUrl'] is None:
            raise ValueError("text must exist if ImgUrl and Img are None")
        return v
