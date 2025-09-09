from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
import os
from dotenv import load_dotenv
import asyncio
from dataclasses import dataclass

# 🔹 Load environment variables
load_dotenv()
set_tracing_disabled(True)

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("API key not found! Please set GEMINI_API_KEY in .env")

# 🔹 Gemini Client
client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 🔹 Model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

# 🔹 Context for users
@dataclass
class UserContext:
    name: str
    role: str  # patient_regular / patient_heavy / admin / guest

# 🔹 Dynamic instructions generator
def generate_instructions(ctx, agent):
    user = ctx.context  

    if user.role == "admin":
        return (
            f"You are assisting Admin {user.name}. "
            "Provide detailed, technical responses with a formal tone."
        )
    elif user.role == "patient_regular":
        return (
            f"You are assisting Patient {user.name}. "
            "They need guidance for regular daily medicines (like diabetes, BP). "
            "Explain schedule, dosage reminders, and importance in very clear, supportive tone."
        )
    elif user.role == "patient_heavy":
        return (
            f"You are assisting Patient {user.name}. "
            "They are prescribed strong / heavy medicines by a doctor. "
            "Explain carefully how they must follow only doctor’s advice, possible side effects, "
            "and safe usage instructions in simple, reassuring tone."
        )
    else:  # guest or default
        return (
            f"You are assisting Guest {user.name}. "
            "Provide short and simple answers, encouraging them to consult a doctor if needed."
        )

# 🔹 Agent
agent = Agent[UserContext](
    name="MedicineHelper",
    model=model,
    instructions=generate_instructions
)

# 🔹 Main runner
async def main():
    # Example contexts: change role here to test
    # context = UserContext(name="Quratulain", role="admin")
    context = UserContext(name="Ali", role="patient_heavy")
    # context = UserContext(name="Sara", role="patient_regular")
    # context = UserContext(name="GuestUser", role="guest")

    result = await Runner.run(
        starting_agent=agent,
        input="Can you explain how I should take my prescribed medicines safely?",
        context=context
    )

    print("\n💊 Final Output:")
    print(result.final_output)

# 🔹 Run
if __name__ == "__main__":
    asyncio.run(main())
