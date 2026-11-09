
import os
import json

from pathlib import Path
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool

from langgraph.checkpoint.memory import InMemorySaver


# 1. Load API key

load_dotenv()

# 2. Initialize our LLM

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)


# 3. Define our storage tool

@tool
def save_student_requirements(
    study_level: str,
    study_areas: list[str],
    preferred_countries: list[str],
    intake: str,
    max_budget_lakhs: float,
    budget_scope: str,
    funding_plan: str,
    priorities: list[str],
    hard_constraints: list[str],
    unresolved_questions: list[str]
) -> str:
    """Save the student's finalized and approved master's requirements."""

    data = {
        "study_level": study_level,
        "study_areas": study_areas,
        "preferred_countries": preferred_countries,
        "intake": intake,
        "max_budget_lakhs": max_budget_lakhs,
        "budget_scope": budget_scope,
        "funding_plan": funding_plan,
        "priorities": priorities,
        "hard_constraints": hard_constraints,
        "unresolved_questions": unresolved_questions
    }

    file_path = Path(__file__).parent / "student_requirements.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return "Student requirements successfully saved."


# 4. Define the agent's role

SYSTEM_PROMPT = """
You are a professional Master's Planning Requirement Analysis Agent.

Your responsibility is to understand the student's requirements
before other agents begin university research or application planning.

Follow this process:

1. Understand the student's educational goals.
2. Extract their preferences, priorities and constraints.
3. Separate hard constraints from preferences.
4. Identify missing information, ambiguities and contradictions.
5. Ask relevant follow-up questions, preferably one at a time.
6. Do not repeatedly ask questions that the student has already answered.
7. Once sufficient information is collected, prepare a clear,
   enhanced requirements summary.
8. Ask the student to review and explicitly approve the summary.
9. Only after explicit approval, call save_student_requirements.

Important:
- Never invent information about the student.
- Do not assume missing information.
- Distinguish confirmed requirements from unresolved questions.
- Do not save unapproved requirements.
- Do not begin university research yourself.
"""


# 5. Create the agent

memory = InMemorySaver()

agent = create_agent(
    model=llm,
    tools=[save_student_requirements],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=memory
)


# 6. Start the conversation

config = {
    "configurable": {
        "thread_id": "student_001"
    }
}

print("Master's Requirement Analysis Agent")
print("Type 'exit' to stop.\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        },
        config=config
    )

    print("\nAgent:", response["messages"][-1].content)
    print()
