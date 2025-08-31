from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

text = """
You are an expert AI research assistant.

Your task is to explain the research paper titled paper_input in a style_input style.  
The explanation should be length_input in length.

Here’s what to include in your explanation:

1. **Core idea of the paper** in the selected style.
2. **Key technical components**, including any important **mathematical formulas** or models.
3. Highlight **common mathematical misunderstandings** or errors that occur when interpreting this paper.
4. Use **clear analogies** or real-world examples when possible to make complex ideas easier to grasp.
5. Make sure the tone and depth match the selected explanation style ("Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical").

Avoid superficial summaries — aim for deep understanding, clarity, and engagement.

Begin your explanation now:
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=0,
)
result = splitter.split_text(text)

print(len(result))
print(result)