from openai import OpenAI

import os
import json  # Import the json module

def send_gpt_json(prompt):
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    
    print('-------------------------------------------------')
    print(prompt)
    print('-------------------------------------------------')

    # Convert the prompt dictionary to a JSON string
    prompt_str = json.dumps(prompt)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", 
             "content": "Analyze the following JSON for patterns in lifestyle that impact emotions and provide insights for a user to learn from. Address your response to the user, and assume they have no knowledge of the website's internals. Only respond with text formatted within HTML so that we can display your analysis on our webpage. " + prompt_str},
        ]
    )
    print('-------------------------------------------------')
    print(response.choices[0].message.content)
    print('-------------------------------------------------')
    
    return response.choices[0].message.content
