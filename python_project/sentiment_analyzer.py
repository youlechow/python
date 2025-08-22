import ollama
import re

def quick_sentiment(text,title,all_text):
    
    prompt = f'Answer in one word only: positive, negative, or neutral. Do not include any explanation. Sentiment of "{text}" based on title "{title}" and content: "{all_text}".'

    response = ollama.generate(
        model='llama2:13b',
        prompt=prompt,
        options={'temperature': 0.01, 'max_tokens': 10}
    )

    raw_output = response['response'].strip()
    cleaned_output = re.sub(r'<think>.*?</think>', '', raw_output, flags=re.DOTALL).strip()
    return cleaned_output.strip().lower()
