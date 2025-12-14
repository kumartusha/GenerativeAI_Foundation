# Problem statement is simple (we have the long text and we want to generate the notes and the quiz from that by executing them in parallel. Also after that we want to merge both of them in single chain and getting the output in which we have the notes, quiz.)


from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableParallel
import os

load_dotenv()

# Define the model
model1 = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROK_API_KEY"))
model2 = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROK_API_KEY"))
model3 = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROK_API_KEY"))

# Define the prompts.
template1 = PromptTemplate(
    template="Generate the proper structured notes using the below content. \n {text}",
    input_variables=["text"]
)

template2 = PromptTemplate(
    template="Generate the proper quiz using the below content. \n {text}",
    input_variables=["text"]
)
template3 = PromptTemplate(
    template="Merge the provided notes and quiz into a single document \n notes -> {notes} and quiz {quiz}",
    input_variables=["notes", "quiz"]
)

# Declare the Parsers.
parser = StrOutputParser()


# Build the entire flow of the project.
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
Pretrained models: Reduce your carbon footprint, compute cost and time by using a pretrained model instead of training an entirely new one. Each pretrained model is reproduced as closely as possible to the original model and offers state-of-the-art performance."""



# Declare the chains.

parallel_chain = RunnableParallel({
    "notes": template1 | model1 | parser,
    "quiz": template2 | model2 | parser
})

merge_chain = template3 | model3 | parser

chain = parallel_chain | merge_chain
result = chain.invoke({"text": text})

# print(result)

chain.get_graph().print_ascii()