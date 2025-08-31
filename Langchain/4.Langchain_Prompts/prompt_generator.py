from langchain_core.prompts import PromptTemplate

template = PromptTemplate(
    template="""
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

Begin your explanation now:
""",
    input_variables=["paper_input", "style_input", "length_input"],
    validate_template=True
)

# Save the template to a file
template.save("template.json")
