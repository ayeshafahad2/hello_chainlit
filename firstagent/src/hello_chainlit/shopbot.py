import chainlit as cl
import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

# -----------------------------
# 1️⃣ Load environment variables
# -----------------------------
load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

# -----------------------------
# 2️⃣ Shop Configuration
# -----------------------------
shop_info = {
    "name": "Ali's Electronics",
    "address": "Main Bazar, Lahore",
    "timings": "Mon-Sat, 10am - 8pm",
    "products": [
        {"name": "LED TV 42 inch", "price": "Rs 55,000"},
        {"name": "Bluetooth Speaker", "price": "Rs 4,500"},
        {"name": "Smartphone XYZ", "price": "Rs 75,000"}
    ]
}

# Convert products list into text for the agent
product_list_text = "\n".join(
    [f"- {p['name']} : {p['price']}" for p in shop_info["products"]]
)

# -----------------------------
# 3️⃣ Provider & Model
# -----------------------------
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

# -----------------------------
# 4️⃣ Agent
# -----------------------------
agent_instructions = f"""
You are a friendly customer service agent for {shop_info['name']}.

Shop details:
Address: {shop_info['address']}
Timings: {shop_info['timings']}
Products & Prices:
{product_list_text}

Rules:
- Always answer politely and with a friendly tone.
- Remember previous user questions in this conversation and use them for context.
- If the user says 'price?' or 'what's the cost?' without naming a product,
  give the price for the product they last mentioned.
- If the user asks about something we don't sell, politely say we don't have it.
"""

agent = Agent(
    name=f"{shop_info['name']} Agent",
    instructions=agent_instructions
)

# -----------------------------
# 5️⃣ Chainlit Events
# -----------------------------
@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        content=f"👋 Hello! Welcome to {shop_info['name']}.\nHow can I help you today?"
    ).send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")

    # Add user message
    history.append({"role": "user", "content": message.content})

    # Run agent with conversation history
    result = await Runner.run(
        agent,
        input=history,
        run_config=run_config
    )

    # Add agent reply to history
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)

    # Send reply
    await cl.Message(content=result.final_output).send()
