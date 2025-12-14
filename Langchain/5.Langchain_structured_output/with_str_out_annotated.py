#. 1. This is the first example of the with_structured_output.
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# from typing import TypedDict, Annotated

# load_dotenv()

# model = ChatOpenAI(model="gpt-4.1-2025-04-14")

# # Schema of the Data
# class Review(TypedDict):

#     """We can give the desc about what we want we dont want to take risk with the LLM because it has trained on huge amount of data."""
    
#     summary: Annotated[str, "A breif summary of the review"]
#     sentiment: Annotated[str, "Return sentiment of the Review either negative, positive and neutral only."]
#     product_information: str

# structured_model = model.with_structured_output(Review)

# result = structured_model.invoke("""The hardware is great, but the software feels bloated. There are too many pre-installed apps that I can't remove. Also, the UI looks outdated compared to other brands. Hoping for a software update to fix this.""")

# print(result)


# 2.  This is the second example of the with_structured_output (Complex Pattern).
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict, Annotated, Optional, Literal
from pydantic import Field
import os

load_dotenv()

# model = ChatOpenAI(model="gpt-4.1-2025-04-14")
model = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROK_API_KEY"))

# schema
class Review(TypedDict):

    key_themes: Annotated[list[str], "Write down all the key themes discussed in the review in a list"]
    summary: Annotated[str, "A brief summary of the review"]
    sentiment: Annotated[Literal["pos", "neg"], "Return sentiment of the review either negative, positive or neutral"]
    pros: Annotated[Optional[list[str]], "Write down all the pros inside a list"]
    cons: Annotated[Optional[list[str]], "Write down all the cons inside a list"]
    name: Annotated[Optional[str], "Write the name of the reviewer"]
    

structured_model = model.with_structured_output(Review)

result = structured_model.invoke("""I recently upgraded to the Samsung Galaxy S24 Ultra, and I must say, it’s an absolute powerhouse! The Snapdragon 8 Gen 3 processor makes everything lightning fast—whether I’m gaming, multitasking, or editing photos. The 5000mAh battery easily lasts a full day even with heavy use, and the 45W fast charging is a lifesaver.

The S-Pen integration is a great touch for note-taking and quick sketches, though I don't use it often. What really blew me away is the 200MP camera—the night mode is stunning, capturing crisp, vibrant images even in low light. Zooming up to 100x actually works well for distant objects, but anything beyond 30x loses quality.

However, the weight and size make it a bit uncomfortable for one-handed use. Also, Samsung’s One UI still comes with bloatware—why do I need five different Samsung apps for things Google already provides? The $1,300 price tag is also a hard pill to swallow.

Pros:
Insanely powerful processor (great for gaming and productivity)
Stunning 200MP camera with incredible zoom capabilities
Long battery life with fast charging
S-Pen support is unique and useful
                                 
Review by Tushar Kumar
""")

print(result)