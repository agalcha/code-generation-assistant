from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate  #vectorstoreindex is a database where we can find data without having to lead the entire pdf file. it uses vector embeddings to convert text to this multidimensional space
from llama_index.core.embeddings import resolve_embed_model  #can load any type of file
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from pydantic import BaseModel
from llama_index.core.output_parsers import  PydanticOutputParser
from llama_index.core.query_pipeline import QueryPipeline
from prompts import context, code_parser_template
from code_reader import code_reader
from dotenv import load_dotenv  #to load environment variables from a .env file into the environment
import ast  #allow us to load python code
import os
import json
import re

load_dotenv()  #load the .env file

llm = Ollama(model = "mistral", request_timeout = 30.0)

parser = LlamaParse(result_type = "markdown")  #documents pushed to the cloud and that parsing is returned to us

file_extractor = {".pdf" : parser}
documents = SimpleDirectoryReader('./data', file_extractor = file_extractor).load_data()  #load all the data from the data folder

embed_model = resolve_embed_model("local:BAAI/bge-m3")  #using this local model cos the defualt for this is ChatGPT which is paid (created vector embeddings for the text)
vector_index = VectorStoreIndex.from_documents(documents, embed_model = embed_model)  #q & a bot
query_engine = vector_index.as_query_engine(llm=llm)

tools = [
    QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="api_documentation",
            description="This gives documentation about code for an API. Use this for reading docs for the API",
        ),
    ),
    code_reader,
]

code_llm = Ollama(model = "codellama")  #this model is for code generation
agent = ReActAgent.from_tools(tools, llm = code_llm, verbose=True, context = context)

class CodeOutput(BaseModel):
    code: str
    description: str
    filename: str

#for formatting it into its json representation so we don't have unnecessary text around it
parser = PydanticOutputParser(CodeOutput)
#json_prompt_str = parser.format(code_parser_template)  #so this format method replaces {response} with the actual response from the llm in the format provided in our class(pydantic model)
# force PromptTemplate to only use {response} as the input variable
json_prompt_tmpl = PromptTemplate(
    template=code_parser_template,
    input_variables = "response"
)

output_pipeline = QueryPipeline(chain=[json_prompt_tmpl, llm])


# Main loop
while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    retries = 0
    cleaned_json = None

    while retries < 3:
        try:
            # Step 1: Query the agent
            result = agent.query(prompt)

            # 🔧 Normalize: guarantee we always have a string
            if isinstance(result, dict):
                # sometimes ReActAgent returns {"response": "..."}
                result_str = result.get("response", str(result))
            else:
                result_str = str(result)
            # Step 2: Run through the pipeline, explicitly passing only the agent's *final* text
                
            #print("📦 Normalized agent result:", repr(result_str))

            next_result = output_pipeline.run(result_str)


            # DEBUG: Show raw output before parsing
            print("🔎 Raw pipeline output:", next_result)

            # Step 3: Parse with pydantic
            cleaned_json = parser.parse(str(next_result))
            break

        except Exception as e:
            retries += 1
            print(f"Error occurred, retry #{retries}:", e)

    if not cleaned_json:
        print("❌ Could not generate valid code output. Try rephrasing your prompt.")
        continue

    # -----------------------
    # Display + Save Output
    # -----------------------
    print("\n✅ Code generated:\n")
    print(cleaned_json.code)
    print("\n📝 Description:", cleaned_json.description)

    filename = cleaned_json.filename
    try:
        os.makedirs("output", exist_ok=True)
        with open(os.path.join("output", filename), "w") as f:
            f.write(cleaned_json.code)
        print(f"💾 Saved file: {filename}")
    except Exception as e:
        print("❌ Error saving file:", e)