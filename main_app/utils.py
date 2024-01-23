from openai import OpenAI

import os
import json  # Import the json module

def send_gpt_json(prompt):
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    
    # Convert the prompt dictionary to a JSON string
    prompt_str = json.dumps(prompt)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", 
            #  "content": "Analyze the following JSON for patterns in lifestyle that impact emotions and provide insights for a user to learn from. Address your response to the user, and assume they have no knowledge of the website's internals. Only respond with text formatted within HTML so that we can display your analysis on our webpage. " + prompt_str},
             "content": "Using the lifestyle and emotional data provided in the following JSON, please identify patterns and correlations between lifestyle factors and reported emotions. Highlight any trends or significant findings that could help the user understand the impact of their daily habits on their emotional health. Offer practical advice or tips for improving well-being based on these insights. Format your response in HTML (no CSS or styling) to include headings, paragraphs, and bullet points for easy reading and comprehension on a webpage. Directly address the user (you). " + prompt_str,
            }
        ]
    )
    
    return response.choices[0].message.content
