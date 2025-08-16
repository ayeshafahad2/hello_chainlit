# import chainlit as cl
# import os
# from dotenv import load_dotenv,find_dotenv
# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,RunConfig

# load_dotenv(find_dotenv())
 
# gemini_api_key = os.getenv("GEMINI_API_KEY")

# provider = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=provider,
# )

# run_config = RunConfig(
#     model=model,
#     model_provider=provider,
#     tracing_disabled=True
# )

# agent = Agent(
#  name="Professional Arabic teacher",
#  instructions="you are a professional arabic teacher help me to learn arabic"
# )

# # run = agent.run( 
# #     "how to say thank you sir ALI jawad Ameen alam kamran tessori ,..teachers and students of GIAICand mainly my husband fahad that i could make this first chatbot .. "
# #     run_config=run_config
# # )

# # result = Runner.run_sync(
# #     input="I am happy",
# #     run_config=run_config,
# #     starting_agent=agent
# # )

# # print(result.final_output)

# @cl.on_message
# async def handle_message(message: cl.Message):
#     result = await Runner.run(
#         agent,
#         input=message.content,
#         run_config=run_config,
#     )

#     await cl.on_Message(content=result.final_output).send()