import json
import logging
import os
import re

from huggingface_hub import InferenceClient

from tools import *

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

TOOLS_TUP = (get_current_time_in_timezone, get_current_weather_info, calculator)

logging.basicConfig(
    filename="agent.log",
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ! SYSTEM_PROMPT beginning
SYSTEM_PROMPT = f"""Answer the following questions as best you can. You have access to the following tools:

{'\n'.join([tool.to_string() for tool in TOOLS_TUP])}

The way you use the tools is by specifying a json blob.
Specifically, this json should have an `action` key (with the name of the tool to use) and a `action_input` key (with the input to the tool going here).

ALWAYS use the following format:

{{
  "action": "$ACTION",
  "action_input": {{"$ARG_NAME": "$ARG_VALUE"}}
}}

Question: the input question you must answer
Thought: you should always think about one action to take. Only one action at a time in this format:
Action:
```
$JSON_BLOB
```
Observation: the result of the action. This Observation is unique, complete, and the source of truth.
... (this Thought/Action/Observation can repeat N times, you should take several steps when needed. The $JSON_BLOB must be formatted as markdown and only use a SINGLE action at a time.)

You must always end your output with the following format:

Thought: I now know the final answer
Final Answer: the final answer to the original input question

ALWAYS finish your response once you defined an action to take (via JSON blob).

Now begin! Reminder to ALWAYS use the exact characters `Final Answer:` when you provide a definitive answer."""
# ! SYSTEM_PROMPT end

agent = InferenceClient(
    model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
    token=HF_API_TOKEN
)

logger.info("Initialized the inference client.")

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

take_input = True
while True:
    if take_input:
        logger.info("Taking user input.")
        user_query = input(">> ")
        if user_query in ["exit", "quit", "q"]:
            break
        messages.append({"role": "user", "content": user_query})
    if take_input:
        logger.info("Sending a prompt.")
    else:
        logger.info("Sending an observation.")
    agent_response = agent.chat.completions.create(
        messages=messages,
        max_tokens=150,
        stop=["Observation:"]  # In case the agent doesn't follow the guidelines.
    )
    response_content = agent_response.choices[0].message.content
    logger.info("Got agent's response.")
    if "Action" in response_content:
        logger.info("The agent is calling an action.")
        json_blob = re.search(r'{.*}', response_content, re.DOTALL).group()
        action_dict = json.loads(json_blob)
        logger.info(f"Got action: {action_dict['action']}")
        res = None
        for tool in TOOLS_TUP:
            if tool.name == action_dict["action"]:
                res = tool(**action_dict["action_input"])
                break
        logger.info(f"Action returned with output: {res}")
        messages.append({"role": "user", "content": f"Observation: {res}"})
        take_input = False
    else:
        take_input = True
        print(response_content)
