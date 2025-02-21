#!/usr/bin/python3
import os
import subprocess

from openai import OpenAI

api_key = os.environ["OPENAI_API_KEY"]
base_url = os.environ.get("OPENAI_API_ENDPOINT", "https://api.openai.com/v1")

client = OpenAI(api_key=api_key, base_url=base_url)
client.base_url = "https://openrouter.ai/api/v1/chat"

model_engine = "gpt-4o"

diff = subprocess.check_output(["git", "diff", "--cached"]).decode("utf-8")

while True:
    prompt = f"Generate a commit message for the following changes:\n{diff}"
    response = client.completions.create(
        model=model_engine, prompt=prompt, max_tokens=50, temperature=0.5, n=1
    )

    generated_text = response.choices[0].text.strip()
    message = generated_text.replace("Commit message:", "").strip()
    print(f"Generated commit message:\n{message}")
    user_input = input("Accept commit message? (y/n/e): ")

    if user_input.lower() == "y":
        subprocess.run(["git", "commit", "-m", message])
        print("Changes committed!")
        break
    elif user_input.lower() == "e":
        edited_text = input("Enter edited commit message: ")
        subprocess.run(["git", "commit", "-m", edited_text])
        print("Changes committed!")
        break
    else:
        print("Regenerating commit message...")
