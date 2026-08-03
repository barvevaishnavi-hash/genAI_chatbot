import os
from dotenv import load_dotenv
from google import genai

# Load .env
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Conversation history
messages = []


def get_response(user_message, pdf_text=""):
    global messages

    try:
        if pdf_text:
            prompt = f"""
You are a helpful AI assistant.

Use the following PDF content to answer the user's question.

PDF Content:
{pdf_text}

User Question:
{user_message}
"""
        else:
            prompt = user_message

        messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        assistant_reply = response.text

        messages.append(
            {
                "role": "assistant",
                "content": assistant_reply
            }
        )

        return assistant_reply

    except Exception as e:
        return f"❌ Error: {e}"


def clear_memory():
    global messages
    messages = []