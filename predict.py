# Example of a predictor for a Hugging Face model using cog (Mixtral 8x7B Instruction Generator)

# Instructions for using the model
# https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1

from cog import BasePredictor, Input, Path
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, GenerationConfig
import transformers
import torch


# This class is part of the predictor needed to work with cog.
class Predictor(BasePredictor):

    # Change all this code to match the model you are using.
    #
    # This is an example of a predictor for a Hugging Face model.

    def setup(self):
        MODEL_NAME = "/src/model_data/"

        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
        )

        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
        self.tokenizer.pad_token = self.tokenizer.eos_token

        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME, torch_dtype=torch.float16,
            trust_remote_code=True,
            device_map="auto",
            quantization_config=quantization_config
        )

        self.generation_config = GenerationConfig.from_pretrained(MODEL_NAME)
        self.generation_config.max_new_tokens = 1024
        self.generation_config.temperature = 0.0001
        self.generation_config.top_p = 0.95
        self.generation_config.do_sample = True
        self.generation_config.repetition_penalty = 1.15

    def predict(self, prompt: str = Input(description="Prompt to generate from")) -> str:
        pipeline = transformers.pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            return_full_text=True,
            generation_config=self.generation_config,
        )

        return pipeline(prompt)[0]["generated_text"]