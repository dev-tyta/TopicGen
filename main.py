from utils.image_utils import load_image, check_url
from utils.caption_utils import ImageCaptioning
from utils.topic_generation import TopicGenerator
import streamlit as st


def main():
    st.title("TopicGen")
    # Create an instance of the TopicGenerator class
    topic_generator = TopicGenerator()
    img_caption = ImageCaptioning()

    # User input
    user_input = st.selectbox(label="Text Input or Image Input", options=["Text", "Image", "Image URL"])
    if user_input == "Text":
        text_input = st.text_input(label="Put in your Idea, Let's generate a matching Topic Sentence🤗🤗")
        generated_topics = topic_generator.generate_topics(text_input)
        for idx, topic in enumerate(generated_topics, 1):
            st.write(f"Topic {idx}: {topic}")
    elif user_input == "Image":
        img_input = st.file_uploader(label="Drop an Image you have been admiring, Let's see what we can do🤔🤔",
                                     type=["jpg", "png", "jpeg"],
                                     accept_multiple_files=True)
        for in_img in img_input:
            if in_img is not None:
                img = load_image(in_img)
                capt = img_caption.get_caption(img)
                st.image(image=img, caption=capt, width=250, height=250)
                generated_topics = topic_generator.generate_topics(capt)
                for idx, topic in enumerate(generated_topics, 1):
                    st.write(f"Topic {idx}: {topic}")

    elif user_input == "Image URL":
        url_input = st.text_input(label="Do you have a link to the Image you would like to drop, Go Ahead and We got "
                                        "you covered😉😉")
        url_img = check_url(url_input)
        img_load = load_image(url_img)
        caption = img_caption.get_caption(img_load)
        st.image(image=img_load, caption=caption, width=250, height=250)
        # Generate and display topics
        generated_topics = topic_generator.generate_topics(caption)
        for idx, topic in enumerate(generated_topics, 1):
            st.write(f"Topic {idx}: {topic}")


if __name__ == "__main__":
    main()
