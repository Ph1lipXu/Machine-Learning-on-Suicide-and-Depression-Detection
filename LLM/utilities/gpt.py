import openai
import os
from openai import OpenAI
from openai import Client

client = OpenAI(
    api_key="YOUR_API_KEY"
)

# Format Text
def formatText(text):
    cleanedText = text.replace("*", "").lower()
    return cleanedText

# Get AI Response
def askGPT(post_body):
    prompt = f"""Given this post body from a post in Reddit forum, 
                please label the author with one of the three labels.

                Please respond as follows:
                1. Reply with "suicide", "depression", or "teenager" 
                   based on which one suits the post topic the best.
                2. On a new line, provide a confidence score (2-decimal double) 
                   between 0 and 1 indicating how confident you are in your decision 
                   (1 is very confident, 0 is not confident).

                Example output:
                depression
                0.85

                Post Body:
                {post_body}
                """

    try:
        # Make the request to the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", 
                       "content": prompt}]
        )
        # Extract and format the response
        gpt_output = response.choices[0].message.content.strip()
        return formatText(gpt_output)
    except Exception as e:
        print(f"Error: {e}")
        return None