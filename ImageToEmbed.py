import os
import numpy as np
from PIL import Image
import torch
from transformers import ViTImageProcessor, ViTModel


class ImageToEmbed:
    def __init__(self):
        # Set seeds for reproducibility
        self._set_seed(42)

        # Initialize device and model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")
        self.model = ViTModel.from_pretrained("google/vit-base-patch16-224").eval().to(self.device)

    def _set_seed(self, seed):
        torch.manual_seed(seed)
        np.random.seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

    # Using last hidden state mean value to get the correct embedding, since pooling layer is not initialized by default and could lead to different results.
    def convert(self, image_path):
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)

        embedding = outputs.last_hidden_state.mean(dim=1).cpu().numpy().flatten()

        return embedding
