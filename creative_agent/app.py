import os
from dotenv import load_dotenv

from agents import Agent, Runner, function_tool, ModelSettings, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled

# 🌿 Load .env
load_dotenv()
set_tracing_disabled(True)

# 🔐 Setup Gemini Client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
external_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)

# 🧠 Model
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

# 🛠️ Tool 1: Price Quote Generator
@function_tool
def generate_quote(service: str, base_price: float, discount: float = 0.0) -> str:
    """Generate a professional price quote for a client."""
    final_price = base_price - (base_price * discount / 100)
    return f"Service: {service}\nBase Price: ${base_price}\nDiscount: {discount}%\nFinal Price: ${final_price}"

# 🛠️ Tool 2: Delivery Estimator
@function_tool
def estimate_delivery(days: int) -> str:
    """Estimate project delivery timeline."""
    return f"Expected delivery time: {days} working days."

# 🛠️ Tool 3: Mood Detector
@function_tool
def detect_mood(message: str) -> str:
    """Detect client's mood based on message tone."""
    message_lower = message.lower()
    if "?" in message or "not sure" in message or "confused" in message_lower:
        return "confused"
    elif "urgent" in message_lower or "asap" in message_lower or "quick" in message_lower:
        return "urgent"
    elif "cost" in message_lower or "price" in message_lower or "serious" in message_lower:
        return "serious"
    else:
        return "friendly"

def main():
    # 🎯 Advanced Client Deal Agent
    client_agent = Agent(
        name="AdvancedClientDealAgent",
        instructions=(
            "You are an adaptive sales assistant. "
            "First detect the client mood using the detect_mood tool. "
            "Then adjust your reply tone:\n"
            "- Confused → explain simply and clearly\n"
            "- Urgent → reply fast, confident & short\n"
            "- Serious → professional, detailed\n"
            "- Friendly → warm, engaging\n"
            "Always aim to build trust and close the deal."
        ),
        model=model,
        tools=[generate_quote, estimate_delivery, detect_mood],
        model_settings=ModelSettings(temperature=0.8)
    )

    # 📝 Example Client Queries
    queries = [
        "I’m confused, can you explain what exactly you provide?",
        "I need a website for my store, urgent ASAP delivery please!",
        "Tell me the exact cost of an ecommerce website.",
        "Hey buddy! I want a nice simple website for my cafe 🙂",
    ]

    for q in queries:
        print(f"\n👤 Client: {q}")
        result = Runner.run_sync(client_agent, q)
        print(f"🤖 Agent: {result.final_output}")

if __name__ == "__main__":
    main()
