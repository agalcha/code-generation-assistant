# 🤖 CodeGen AI Agent

An AI buddy that reads your docs, understands your code, and even writes new code for you.

---

## ✨ What It Does

- Reads your **API docs** (PDFs) like a champ  
- Peeks into your **code files** to understand what’s already there  
- Embeds all that knowledge into a searchable vector DB (fancy way of saying: *it remembers stuff*)  
- Takes natural language prompts like *“write me a Python script that calls the POST endpoint”*  
- Gives clean JSON with:
  - `code` → The actual Python code  
  - `description` → What the code does in plain English  
  - `filename` → Where it’ll live  
- Saves everything neatly into an `output/` folder 

---

## Quickstart

1. **Clone this repo:**  
<pre>git clone https://github.com/<your-username>/codegen-ai-agent.git  
cd codegen-ai-agent</pre>

2. **Set up your virtual environment:**
<pre>python3 -m venv ai  
source ai/bin/activate</pre>  

3. **Install the magic sauce:**  
<pre>pip install -r requirements.txt  </pre>

4. **Add your api key to .env:**  
OLLAMA_API_KEY=your_api_key_here

5. **Run it:**   
<pre>python3 main.py</pre>

6. **Now you can talk to your AI Agent directly:**  
Enter a prompt (q to quit):  
➡ read test.py and generate a new client script for the API

## 🗂 **Project Layout**
CODE_GEN_AGENT/
├─ data/           # Drop your PDFs or code files here  
├─ output/         # AI-generated code goes here  
├─ main.py         # The brain  
├─ prompts.py      # Custom prompts for the AI  
├─ code_reader.py  # Lets AI actually read your code  
└─ requirements.txt

## 🛠 **Built With**  
llama-index — for document + vector embeddings  
Ollama — local LLMs like mistral and codellama  
Pydantic — keeping JSON output squeaky clean
