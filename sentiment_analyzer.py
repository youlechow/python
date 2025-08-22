import ollama
import re

def quick_sentiment(text,title,all_text):
    
    prompt = f'Answer with one of the following sentiments: positive, negative, or neutral. Then provide a short explanation. Sentiment of "{text}" based on title "{title}" and content: "{all_text}".'

    response = ollama.generate(
        model='llama2:13b',
        prompt=prompt,
        options={'temperature': 0.01, 'max_tokens': 100,'top_p':1.0}
    )

    raw_output = response['response'].strip()
    cleaned_output = re.sub(r'<think>.*?</think>', '', raw_output, flags=re.DOTALL).strip()
    return raw_output.strip().lower()
