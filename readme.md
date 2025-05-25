from dotenv import load_dotenv
from openai import OpenAI
import os

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

user = "Hey, What is the weather of patiala"

print_user = client.chat.completions.create(
    model = "gemma2-9b-it",
    messages = [{"role": "system", "content": f"You are a helpfull ai assistant who generates 3 more questions based on present user input. user input, {user}"}, {"role": "user", "content": user}] 
)

print(print_user.choices[0].message.content)
        
