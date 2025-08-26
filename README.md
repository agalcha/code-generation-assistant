# 🤖 CodeGen AI Agent

*An AI buddy that reads your docs, understands your code, and even writes new code for you.*  
No more scrolling through PDFs or manually wiring up boilerplate. Just ask, and it builds.  

---

## ✨ What It Does

- 📚 Reads your **API docs** (PDFs) like a champ  
- 🧑‍💻 Peeks into your **code files** to understand what’s already there  
- 🔍 Embeds all that knowledge into a searchable vector DB (fancy way of saying: *it remembers stuff*)  
- 🪄 Takes natural language prompts like *“write me a Python script that calls the POST endpoint”*  
- 📝 Spits out clean JSON with:
  - `code` → The actual Python code  
  - `description` → What the code does in plain English  
  - `filename` → Where it’ll live  
- 💾 Saves everything neatly into an `output/` folder for you  

---

## 🚀 Quickstart

1. **Clone this repo:**  
git clone https://github.com/<your-username>/codegen-ai-agent.git  
cd codegen-ai-agent

2. **Set up your virtual environment:**
python3 -m venv ai  
source ai/bin/activate  # macOS / Linux  
ai\Scripts\activate     # Windows

3. **Install the magic sauce:**  
pip install -r requirements.txt  
Add your secrets to .env:  
OLLAMA_API_KEY=your_api_key_here

4. **Run it:**  
python3 main.py

5. **Now you can talk to your AI Agent directly:**  
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
