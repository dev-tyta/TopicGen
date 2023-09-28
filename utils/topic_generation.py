import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
device = "cuda" if torch.cuda.is_available() else "cpu"


class TopicGenerator:

    def __init__(self):
        # Initialize tokenizer and model upon class instantiation
        self.tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")
        self.model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large").to(device)  # assuming you have a GPU available

    def generate_topics(self, user_input, num_topics=3):
        """
        Generate topic sentences based on the user input.

        Args:
        - user_input (str): The input text provided by the user.
        - num_topics (int, optional): Number of topics to generate. Defaults to 3.

        Returns:
        - list: A list of generated topic sentences.
        """
        prompt_text = f"Generate a topic sentence based on the following input: {user_input}"
        input_ids = self.tokenizer(prompt_text, return_tensors="pt").input_ids.to(device)

        # Generate topics
        outputs = self.model.generate(input_ids, do_sample=True, top_k=50, temperature=0.7, max_length=50, num_return_sequences=num_topics)

        # Decode the outputs and return as a list of topic sentences
        return [self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
