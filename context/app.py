from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    RunContextWrapper,
    function_tool
)
from dataclasses import dataclass
from dotenv import load_dotenv
import os
import asyncio

# ✅ Environment Setup
load_dotenv()
set_tracing_disabled(disabled=True)

# 🔑 API KEY Setup
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise KeyError("Error 405: API key not found")

# 🌐 Gemini Client
client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

# 📅 Calendar Reminder Schema
@dataclass
class CalendarReminder:
    title: str
    date: str
    time: str
    location: str
    description: str

# 🛠️ Tool: Fetch calendar reminder
@function_tool
async def get_calendar_reminder(ctx: RunContextWrapper[CalendarReminder]) -> str:
    """
    Returns the details of the user's calendar reminder.
    """
    reminder = ctx.context  # CalendarReminder object
    return (
        f"📌 Reminder: {reminder.title}\n"
        f"📅 Date: {reminder.date}\n"
        f"⏰ Time: {reminder.time}\n"
        f"📍 Location: {reminder.location}\n"
        f"📝 Notes: {reminder.description}"
    )


# 🧠 Shallow vs Deep Type Explanation
"""
👉 Shallow Type:
   - Sirf basic data structures ko define karta hai (surface-level).
   - Example: str, int, list, dict.
   - Agar hum CalendarReminder ko simple dictionary bana dete:
        reminder = {"title": "Meeting", "date": "2025-08-25"}
     Yeh SHALLOW type hai, kyunki validation aur structure enforce nahi hota.

👉 Deep Type:
   - Proper schema / dataclass banake strong typing deta hai.
   - Har attribute ka type fix hota hai (string, date, etc).
   - Example: @dataclass CalendarReminder jisme title, date, time fields fix hain.
   - Yeh enforce karta hai ke reminder hamesha correct structure follow kare.
   - Agents SDK mein deep type helpful hota hai taake model ko structured context mile.
"""

# 🚀 Main Function
async def main():
    # Example Calendar Reminder Data (Deep Type - dataclass based)
    reminder = CalendarReminder(
        title="Project Meeting",
        date="2025-08-25",
        time="10:00 AM",
        location="Zoom",
        description="Discuss Q3 targets and AI integration plan."
    )

    # Agent Creation
    agent = Agent[CalendarReminder](
        name="CalendarAssistant",
        tools=[get_calendar_reminder],
        model=model,
    )

    # Run Agent
    result = await Runner.run(
        starting_agent=agent,
        input="Show me my calendar reminder details.",
        context=reminder,
    )

    # Print Result
    print(result.final_output)


# ⏳ Entry Point
if __name__ == "__main__":
    asyncio.run(main())
