# This is the code for downloading the model.

from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace

llm = HuggingFacePipeline.from_model_id(
    model_id="meta-llama/Llama-3.2-1B-Instruct",
    task="text-generation",
    pipeline_kwargs=dict(temperature=0.3, max_new_tokens=100 )
)
 
model = ChatHuggingFace(llm = llm)

print(model.invoke("What is the Capital of India ??"))