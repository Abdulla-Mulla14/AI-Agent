from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key = os.getenv('GROQ_API_KEY')
)
    

def getWeatherDetails(city = ''):
    if city == "patiala": return '10°C'
    if city == "manali": return '14°C'
    if city == "bangalore": return '8°C'
    if city == "mumbai": return '5°C'
    if city == "delhi": return '6°C'

tools = {
    "getWeatherDetails": getWeatherDetails
}

SYSTEM_PROMPT = '''
    You are an AI Assistant with START, PLAN, ACTION, OBSERVATION and OUTPUT State.
    Wait for the user prompt and first PLAN using available tools.
    After Planning, Take the action with appropriate tools and wait for Observation based on Action.
    Once you get Observation, Return the AI response based on START prompt and observations

    Strictly follow the JSON output format as in examples

    Available Tools:
    - def getWeatherDetails(city: string): string
    getWeatherDetails is a function that accepts city name as string and returns the weather details

    Example:
    START 
    {"type": "user", "user": "What is the sum of weather of Patiala and Mohali"}
    {"type": "plan", "plan": "I will call the getWeatherDetails for Patiala"}
    {"type": "action", "function": "getWeatherDetails", "input": "Patiala"}
    {"type": "observation", "observation": "10°C"}
    {"type": "plan", "plan": "I will call the getWeatherDetails for Mohali"}
    {"type": "action", "function": "getWeatherDetails", "input": "Mohali"}
    {"type": "observation", "observation": "14°C"}
    {"type": "output", "output": "The sum of weather of Patiala and Mohali is 24°C"}

'''
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Give me the weather in Bangalore as a JSON object with city, temperature, and condition."}
]

while True:
    query = input('>> ')
    q = {
        "type": 'user',
        "user": query,
    }
    messages.append({"role": "user", "content": json.dumps(q)})

    while True:
        chat = client.chat.completions.create(
            model = "gpt-4o",
            messages = messages,
            response_format = {"type": "json_object"} 
        )

        result = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": result})

        call = json.loads(result)

        if call["type"] == "output":
            print("bot_says: " + str(call.output))
            break
        elif call["type"] == "action":
            fn = tools[call["function"]]
            observation = fn[call["input"]]
            obs = {"type": "observation", "observation": observation}
            messages.append({"role": "developer", "content": json.dumps(obs)})


