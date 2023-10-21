import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
word_1 = '付き合う'
word_2 = '罷り通る'
response = openai.ChatCompletion.create(
    model = "gpt-4",
    messages=[
    {"role": "user", "content": f"Compose an example sentence using \"{word_2}\" without any additional explanation."}
  ]
)
print(response['choices'][0]['message']['content'])