import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from utils.image_utils import load_image

device = "cuda" if torch.cuda.is_available() else "cpu"


class ImageCaptioning:

    def __int__(self):
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

    def get_caption(self, image_path):
        image = load_image(image_path)

        # Preprocessing the Image
        img = self.processor(image, return_tensors="pt").to(device)

        # Generating captions
        output = self.model.generate(**img)

        # decode the output
        caption = self.processor.batch_decode(output, skip_special_tokens=True)[0]

        return caption
