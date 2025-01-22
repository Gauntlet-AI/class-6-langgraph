from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import END, MessageGraph
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

model = ChatOpenAI(temperature=0, model="gpt-4o-mini")

# First, we initialize our model and a MessageGraph.
graph = MessageGraph()

# Next, we add a single node to the graph,
# called "oracle", which simply calls the model with the given input.
graph.add_node("oracle", model)

# We add an edge from this "oracle" node to the special string END ("__end__").
# This means that execution will end after the current node.
graph.add_edge("oracle", END)

# We set "oracle" as the entrypoint to the graph.
graph.set_entry_point("oracle")

# We compile the graph
runnable = graph.compile()

# How state moves through the graph:
# 1. LangGraph adds the input message to the internal state.
# 2. Then passes the state to the entrypoint node, "oracle".
# 3. The "oracle" node executes, invoking the chat model.
# 4. The chat model returns an AIMessage. LangGraph adds this to the state.
# 5. Execution progresses to the special END value and outputs the final state.
response = (runnable.invoke(HumanMessage("What is 1 + 1?")))
print(response[1].content)
