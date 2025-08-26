from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",   # or just "claude-3.5-sonnet"
    temperature=0.1,
    max_tokens=1000,
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

print(llm.invoke("Hey buddy, how are you?"))