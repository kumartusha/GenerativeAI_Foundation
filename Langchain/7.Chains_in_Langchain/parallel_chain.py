# Here we will be build the Sequential chain using the LLM.
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableParallel
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()

model1 = ChatOpenAI(model='gpt-4o-mini')

# model2 = ChatAnthropic(model_name='claude-opus-4-20250514')
model2 = ChatOpenAI(model='gpt-3.5-turbo')
# model2 = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", api_key=os.getenv("GOOGLE_API_KEY"))

prompt1 = PromptTemplate(
    template="Generate Short and simple notes from the following text \n {text}",
    input_variables=['text']
)
 
prompt2 = PromptTemplate(
    template="Generate 5 short question answers from the following text \n {text}",
    input_variables=['text']
)

prompt3 = PromptTemplate(
    template="Merge the provided notes and quiz into a single document \n notes -> {notes} and quiz {quiz}",
    input_variables=['notes','quiz']
)

parser = StrOutputParser()

# 
parallel_chain = RunnableParallel({
    'notes': prompt1 | model1 | parser,
    'quiz': prompt2 | model2 | parser
})

merge_chain = prompt3 | model1 | parser

chain = parallel_chain | merge_chain


text = """Transformers acts as the model-definition framework for state-of-the-art machine learning models in text, computer vision, audio, video, and multimodal model, for both inference and training.

It centralizes the model definition so that this definition is agreed upon across the ecosystem. transformers is the pivot across frameworks: if a model definition is supported, it will be compatible with the majority of training frameworks (Axolotl, Unsloth, DeepSpeed, FSDP, PyTorch-Lightning, …), inference engines (vLLM, SGLang, TGI, …), and adjacent modeling libraries (llama.cpp, mlx, …) which leverage the model definition from transformers.

We pledge to help support new state-of-the-art models and democratize their usage by having their model definition be simple, customizable, and efficient.

There are over 1M+ Transformers model checkpoints on the Hugging Face Hub you can use.

Explore the Hub today to find a model and use Transformers to help you get started right away.

Features
Transformers provides everything you need for inference or training with state-of-the-art pretrained models. Some of the main features include:

Pipeline: Simple and optimized inference class for many machine learning tasks like text generation, image segmentation, automatic speech recognition, document question answering, and more.
Trainer: A comprehensive trainer that supports features such as mixed precision, torch.compile, and FlashAttention for training and distributed training for PyTorch models.
generate: Fast text generation with large language models (LLMs) and vision language models (VLMs), including support for streaming and multiple decoding strategies.
Design
Read our Philosophy to learn more about Transformers’ design principles.

Transformers is designed for developers and machine learning engineers and researchers. Its main design principles are:

Fast and easy to use: Every model is implemented from only three main classes (configuration, model, and preprocessor) and can be quickly used for inference or training with Pipeline or Trainer.
Pretrained models: Reduce your carbon footprint, compute cost and time by using a pretrained model instead of training an entirely new one. Each pretrained model is reproduced as closely as possible to the original model and offers state-of-the-art performance.
"""

result = chain.invoke({'text': text})

# print(result)

chain.get_graph().print_ascii()
