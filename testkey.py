import google.generativeai as genai
import os

api_key = "AIzaSyAaTPCYVLr6NthIrQds8mO8BfyJ9_XBkA0" 

genai.configure(api_key=api_key)

print("Checking available models for this key...")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            
except Exception as e:
    print(f"Error: {e}")