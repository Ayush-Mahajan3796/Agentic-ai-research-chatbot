from langchain_community.tools import WikipediaQueryRun,ArxivQueryRun
from langchain_community.utilities import WikipediaAPIWrapper,ArxivAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from typing import Annotated
from langgraph.graph.message import add_messages
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

api_wrapper_arxiv=ArxivAPIWrapper(top_k_results=2,doc_content_chars_max=500)
arxiv=ArxivQueryRun(api_wrapper=api_wrapper_arxiv,description="query arxiv papers")
api_wrapper_wikipedia=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=500)
wiki=WikipediaQueryRun(api_wrapper=api_wrapper_wikipedia)
tavily = TavilySearchResults(tavily_api_key="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")
from dotenv import load_dotenv
load_dotenv()
import os

os.environ["TAVILY_API_KEY"]=os.getenv("TAVILY_API_KEY")
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

tools=[arxiv,wiki,tavily]
llm=ChatGroq(model="qwen/qwen3-32b")
llm_with_tools=llm.bind_tools(tools=tools)

class State(TypedDict):
    messages:Annotated[list[AnyMessage],add_messages]

def tool_calling(state:State):
    return {"messages":[llm_with_tools.invoke(state["messages"])]}

builder=StateGraph(State)
builder.add_node("tool_calling",tool_calling)
builder.add_node("tools",ToolNode(tools))

builder.add_edge(START, "tool_calling")
builder.add_conditional_edges("tool_calling",tools_condition,)
builder.add_edge("tools",END)
graph=builder.compile()

def get_ai_response(user_input):
    messages = graph.invoke({"messages": user_input})
    return [str(m.content) for m in messages["messages"]]