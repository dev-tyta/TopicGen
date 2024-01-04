from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from schemas import TopicGenInputSchema
from utils.caption_utils import ImageCaptioning
from utils.topic_generation import TopicGenerator
from utils.image_utils import load_image, check_url

app = FastAPI(
    title=settings.PROJECT_NAME,
)

# CORS
if settings:
    app.add_middleware(
        CORSMiddleware,
        allow_origins='*',
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

topic_generator = TopicGenerator()
img_caption = ImageCaptioning()


@app.get("/")
async def root():
    return {"message": "Welcome To TopicGen API"}


@app.get("/health")
async def health():
    return {"message": "OK"}


@app.get("/generate")
async def generate_topic(
    data: TopicGenInputSchema
):
    # if only text is provided
    if data.text is not None and data.Img is None and data.url is None:
        generated_topics = topic_generator.generate_topics(data.text)
        return {"topics": generated_topics}

    # if only image is provided
    elif data.Img or data.ImgUrl is not None and data.text is None:
        if data.Img:
            img = load_image(data.Img)
        elif data.ImgUrl:
            img_url = check_url(data.ImgUrl)
            img = load_image(img_url)
        capt = img_caption.get_caption(img)
        generated_topics = topic_generator.generate_topics(capt)
        return {"topics": generated_topics}

    # if both text and image are provided
    elif data.text is not None and data.Img or data.ImgUrl is not None:
        if data.Img:
            img = load_image(data.Img)
        elif data.ImgUrl:
            img_url = check_url(data.ImgUrl)
            img = load_image(img_url)
        capt = img_caption.get_caption(img)
        text_and_img_caption = data.text + ". " + capt
        generated_topics = topic_generator.generate_topics(
            text_and_img_caption
        )
        return {"topics": generated_topics}
