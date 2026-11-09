from groq import Groq
from dotenv import load_dotenv
import os
import json
from tools import calculate_total_tuition

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_total_tuition",
            "description": "Calculate the total of multiple university tuition fees.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fees": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "List of tuition fees in lakhs."
                    }
                },
                "required": ["fees"]
            }
        }
    }
]

messages = [
    {
        "role": "user",
        "content": "Calculate the total tuition fees for universities costing 12 lakh, 15 lakh and 18 lakh."
    }
]

# First LLM request
response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# Get the LLM's response
message = response.choices[0].message

# Add the assistant's response to conversation history
messages.append(message)

# Execute requested tools
if message.tool_calls:

    for tool_call in message.tool_calls:

        tool_name = tool_call.function.name

        arguments = json.loads(tool_call.function.arguments)

        if tool_name == "calculate_total_tuition":
            result = calculate_total_tuition(**arguments)

            # Send tool result back to the LLM
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

# Second LLM request
final_response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=messages
)

print("Final answer:")
print(final_response.choices[0].message.content)