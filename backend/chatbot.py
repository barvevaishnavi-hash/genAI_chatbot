import ollama

messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful AI assistant. "
            "Answer in simple, student-friendly language. "
            "For programming questions, provide examples. "
            "Keep answers clear, concise, and well formatted."
        )
    }
]


def get_response(user_message, pdf_text=""):
    global messages

    # If a PDF is uploaded, add its content to the prompt
    if pdf_text:
        user_message = f"""
Use the following PDF to answer the question.

PDF Content:
{pdf_text}

Question:
{user_message}

If the answer is not available in the PDF,
say:
'I couldn't find this information in the uploaded PDF.'
"""

    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    response = ollama.chat(
        model="llama3.2:1b",
        messages=messages
    )

    assistant_reply = response["message"]["content"]

    messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )

    return assistant_reply


def clear_memory():
    global messages
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI assistant. "
                "Answer in simple, student-friendly language. "
                "For programming questions, provide examples. "
                "Keep answers clear, concise, and well formatted."
            )
        }
    ]