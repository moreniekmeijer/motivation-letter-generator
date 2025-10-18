# gemini_client.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialiseer de Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


def generate_motivation_letter(user_info: str, job_description: str) -> str:
    prompt = f"""
You are a professional AI assistant that writes job application and motivation letters in English.

User information:
{user_info}

Job description:
{job_description}

Write a clear, professional, and enthusiastic motivation letter in English. 
Include: introduction, key strengths, and a polite closing.
Output only the letter, no explanations.
"""
    # Direct aanroepen van het LLM object
    response = llm.invoke(prompt)
    return response.content
