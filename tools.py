"""
The agent's toolbox.

Each tool is two things:
  1. A SCHEMA  -> what the model sees (name, description, parameters).
     The description is how the model decides WHEN to use the tool, so write it well.
  2. A FUNCTION -> the real code that runs when the model asks for that tool.

The schemas use the OpenAI-style "function" shape, because that's what Groq speaks
(and most other providers too). If you switch providers, the JSON schema inside
"parameters" usually stays exactly the same — only the wrapper changes.

TOOL_SCHEMAS is the menu handed to the model.
TOOL_FUNCTIONS maps a tool name to the function that does the work.
"""

import os
import datetime
from groq import Groq
from dotenv import load_dotenv
import requests

import config

load_dotenv()

# One shared client for tools that need to call the model (e.g. research).
# Groq() reads GROQ_API_KEY from the environment — never pass a key here.
_client = Groq()

web_search_schema = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search the web for recent information and return useful search results.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query."
                }
            },
            "required": ["query"]
        }
    }
}

def web_search(query: str) -> str:
    api_key = os.getenv("TAVILY_API_KEY")

    url = "https://api.tavily.com/search"

    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "max_results": 5
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        return response.text

    data = response.json()

    text = ""

    for result in data.get("results", []):
        text += f"Title: {result['title']}\n"
        text += f"Content: {result['content']}\n"
        text += f"Source: {result['url']}\n\n"

    return text
# ---------------------------------------------------------------------------
# TOOL 1 — research
# ---------------------------------------------------------------------------

research_schema = {
    "type": "function",
    "function": {
        "name": "research",
        "description": (
            "Research a topic and return a short, factual set of notes about it. "
            "Use this when you need information before writing anything."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The subject to research, e.g. 'the James Webb telescope'.",
                }
            },
            "required": ["topic"],
        },
    },
}


def research(topic: str) -> str:
    search_results = web_search(topic)

    prompt = f"""
You are a research assistant.

Using the following web search results, write short research notes.

{search_results}

Keep them clear, factual and in bullet points.
"""

    response = _client.chat.completions.create(
        model=config.MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=1000
    )

    return response.choices[0].message.content

# ---------------------------------------------------------------------------
# TOOL 2 — save_note  (fully working, nothing to change)
# ---------------------------------------------------------------------------

save_note_schema = {
    "type": "function",
    "function": {
        "name": "save_note",
        "description": (
            "Save text to a note file so it can be reused later. "
            "Use this to store research findings before writing a summary."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "File name only, e.g. 'webb-notes.md'. No folders.",
                },
                "content": {
                    "type": "string",
                    "description": "The text to save.",
                },
            },
            "required": ["filename", "content"],
        },
    },
}


def save_note(filename: str, content: str) -> str:
    """Write `content` to notes/<filename>. Stays inside the notes folder on purpose."""
    os.makedirs(config.NOTES_DIR, exist_ok=True)

    # Safety: strip any path tricks so a note can only ever land in notes/.
    safe_name = os.path.basename(filename)
    path = os.path.join(config.NOTES_DIR, safe_name)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Saved {len(content)} characters to {path}"


# ---------------------------------------------------------------------------
# TOOL 3 — send_email  (dry-run by default; the approval gate protects it)
# ---------------------------------------------------------------------------

send_email_schema = {
    "type": "function",
    "function": {
        "name": "send_email",
        "description": (
            "Send an email summary to a recipient. "
            "Use this as the final step once the notes are ready."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "Recipient email address."},
                "subject": {"type": "string", "description": "Email subject line."},
                "body": {"type": "string", "description": "The full email body."},
            },
            "required": ["to", "subject", "body"],
        },
    },
}


def send_email(to: str, subject: str, body: str) -> str:
    """
    STARTER VERSION: DRY RUN. It does not send anything — it just prints what it
    WOULD send. That's on purpose: nobody spams a real inbox while building.

    TODO (stretch): wire up a real send only if you want to. Safer options than
    raw SMTP: a Gmail MCP connector, or a transactional email API. Whatever you use,
    keep this tool behind the human approval gate.
    """
    when = datetime.datetime.now().strftime("%H:%M:%S")
    print("\n----- DRY-RUN EMAIL -------------------------------")
    print(f"time:    {when}")
    print(f"to:      {to}")
    print(f"subject: {subject}")
    print("body:")
    print(body)
    print("---------------------------------------------------\n")
    return f"(dry-run) email to {to} prepared but not actually sent"


# ---------------------------------------------------------------------------
# Registries the agent uses.
# ---------------------------------------------------------------------------

TOOL_SCHEMAS = [
    web_search_schema,
    research_schema,
    save_note_schema,
    send_email_schema,
]

TOOL_FUNCTIONS = {
    "web_search": web_search,
    "research": research,
    "save_note": save_note,
    "send_email": send_email,
}