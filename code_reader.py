#this tool exists cos the parser we're using actually doesn't read code files like .py .js .java etc. so we create a custom tool to read these files
from llama_index.core.tools import FunctionTool  #wrap any python func as a tool and pass it to the llm
import os


def code_reader_func(file_name):
    path = os.path.join("data", file_name)
    try:
        with open(path, "r") as f:
            content = f.read()
            return {"file_content": content}
    except Exception as e:
        return {"error": str(e)}
    
code_reader = FunctionTool.from_defaults(
    fn=code_reader_func,
    name="code_reader",
    description="""this tool can read the contents of code files and return 
    their results. Use this when you need to read the contents of a file""",
)