from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

client = OpenAI(api_key=SECRET_KEY)
        
def get_api_response(prompt: str) -> str | None:
    text: str | None = None
    
    try:
        response = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[
            {
              "role": "system",
              "content": "Hello\n"
            },
            {
              "role": "user",
              "content": "Hello"
            }
          ],
          temperature=0.9,
          max_tokens=256,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0.6,
          stop=["Human:", "AI:"]
        )
        
        choices: dict = response.get('choises')[0]
        text = choices.get('text')
    except Exception as e:
        print('Error',e)
        
        return text

def update_list(message: str, pl: list[str]):
  pl.append(message)
  
def create_prompt(message: str, pl: list[str]) -> str:
  p_message: str = f'\nHuman: {message}'
  update_list(p_message, pl)
  prompt: str = ''.join(pl)
  return prompt

def get_bot_response(message: str, pl: list[str]) -> str:
  prompt: str = create_prompt(message, pl)
  bot_response: str = get_api_response(prompt)
  
  if bot_response:
    update_list(bot_response, pl)
    pos: int = bot_response.find('\nAI: ')
    bot_response = bot_response[pos + 5:]
  else:
    bot_response = 'Something went Wrong ......'
    
  return bot_response

def main():
  prompt_list: list[str] = ['You will pretend to be a person dude that ends every response with "homie?"',
                            '\nHuman: What country is it?',
                            '\nAI: It is Sri Lanka, homies']
  while True:
    user_input: str = input('You: ')
    response: str = get_bot_response(user_input, prompt_list)
    print(f'Bot: {response}')
    

if __name__ == '__main__':
  main()