🤖 Personal Task Agent

A Python-based AI Agent that completes a multi-step task automatically using Large Language Models (LLMs), external tools, and safety guardrails.

The agent can research a topic, generate useful notes, save them into files, and prepare an email summary while keeping a human approval step for sensitive actions.

📌 Features

- 🔍 Web research using Tavily Search API
- 🧠 AI-powered research summarization using Groq LLM
- 📝 Generate concise research notes
- 💾 Save notes automatically into files
- ✅ Human approval before sensitive actions
- 📧 Email summary workflow with approval control
- 📋 Detailed execution logs
- 🛡️ Safety guardrails:
  - Approval gate
  - Logging
  - Maximum iteration limit

🛠️ Tech Stack

- Python 3.x
- Groq API
- Tavily Search API
- OpenAI-style Function Calling
- python-dotenv
- Requests

📂 Project Structure

personal-task-agent/

│── agent.py          # Main agent loop with reasoning, tools, approval & logging
│── tools.py          # Agent tools (web search, research, save notes, email)
│── config.py         # Model settings and safety controls
│── requirements.txt  # Project dependencies
│── .env              # API keys (not uploaded to GitHub)
│── notes/            # Saved research notes
│── logs/             # Execution logs
│── README.md         # Project documentation

⚙️ Installation

1. Clone Repository

git clone https://github.com/yourusername/personal-task-agent.git

cd personal-task-agent

2. Create Virtual Environment

python -m venv venv

Activate:

Windows:

venv\Scripts\activate

Linux/macOS:

source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

🔑 Environment Variables

Create a ".env" file in the project folder:

GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key

Never upload ".env" because it contains private API keys.

🚀 Running the Agent

Run:

python agent.py "Research Artificial Intelligence, save notes to ai.md, then email a summary"

🧠 Workflow

User Goal
    │
    ▼
AI Agent Reasoning
    │
    ▼
Web Search Tool
    │
    ▼
Research Summary
    │
    ▼
Save Notes
    │
    ▼
Human Approval
    │
    ▼
Email Action
    │
    ▼
Execution Logs

🛡️ Guardrails

This project includes:

- Human approval before risky actions
- Automatic logging of every tool call
- Maximum iteration limit to prevent infinite loops
- Environment variable protection

📄 Generated Files

Notes

Research results are saved inside:

notes/

Logs

Agent execution history is stored inside:

logs/

Logs include:

- Tool calls
- Results
- Approvals
- Timestamps

🎯 Learning Outcomes

This project demonstrates:

- AI Agent architecture
- LLM tool calling
- Multi-step task automation
- Human-in-the-loop systems
- API integration
- File handling
- Logging and safety mechanisms

🔮 Future Improvements

- Real email integration
- Streamlit web interface
- PDF report generation
- Database storage
- Voice-based interaction
- More AI tools integration

👩‍💻 Author

Sadia Shabir

Information Technology Student | AI & Automation Learner

📜 License

This project is created for educational purposes and learning
