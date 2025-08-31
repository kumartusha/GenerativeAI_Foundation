from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import streamlit as st

load_dotenv()
model = ChatOpenAI()

st.header("Research Tool")

paper_input = st.selectbox("Select Research Paper Name", ["Select....", "Attention is all you need", "BERT: Pre-trained BERT model","GPT-3: Pre-trained GPT-3 model","Diffusion Models Beat GANs on Image Synthesis"])

style_input = st.selectbox("Select Explanation Style", ["Select....", "Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"])

length_input = st.selectbox("Select Explanation Length", ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"])

# First method to use the prompt.
template = PromptTemplate(template=f"""
You are an expert AI research assistant.

Your task is to explain the research paper titled {paper_input} in a {style_input} style.  
The explanation should be {length_input} in length.

Here’s what to include in your explanation:

1. **Core idea of the paper** in the selected style.
2. **Key technical components**, including any important **mathematical formulas** or models.
3. Highlight **common mathematical misunderstandings** or errors that occur when interpreting this paper.
4. Use **clear analogies** or real-world examples when possible to make complex ideas easier to grasp.
5. Make sure the tone and depth match the selected explanation style ("Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical").

Avoid superficial summaries — aim for deep understanding, clarity, and engagement.

Begin your explanation now:""", input_variables=[paper_input, style_input, length_input], validate_template=True)

# Second way to use the prompt Template.
# template = load_template("Json File name")

prompt = template.format(paper_input=paper_input, style_input=style_input, length_input=length_input)

if st.button("Submit"):
    result = model.invoke(prompt)
    st.write(result.content)