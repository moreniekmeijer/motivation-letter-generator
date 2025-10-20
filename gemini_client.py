import os
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

intro_prompt = PromptTemplate.from_template("""
You are writing the introduction paragraph for a professional motivation letter.
It should sound personal, enthusiastic, and relevant.

User information:
{user_info}

Write only the introduction paragraph.
""")

strengths_prompt = PromptTemplate.from_template("""
Continue the motivation letter naturally after the introduction below.

Introduction:
{intro}

Now write a paragraph describing 2–3 of the user's key strengths, achievements, or professional qualities.
Keep the same tone and flow.

User information:
{user_info}
""")

match_prompt = PromptTemplate.from_template("""
Continue the motivation letter naturally after the previous paragraphs.

Introduction:
{intro}

Strengths:
{strengths}

Now write a paragraph explaining how the user's experience and skills align with the job description.

Job description:
{job_description}
""")

closing_prompt = PromptTemplate.from_template("""
You are finishing a motivation letter that currently contains the following paragraphs:

Introduction:
{intro}

Strengths:
{strengths}

Alignment:
{match}

Write a polite, optimistic closing paragraph that fits naturally with the rest of the letter.
""")


def generate_motivation_letter(user_info: str, job_description: str) -> str:
    intro = (intro_prompt | llm).invoke({"user_info": user_info})
    strengths = (strengths_prompt | llm).invoke({
        "intro": intro.content,
        "user_info": user_info
    })
    match = (match_prompt | llm).invoke({
        "intro": intro.content,
        "strengths": strengths.content,
        "user_info": user_info,
        "job_description": job_description
    })
    closing = (closing_prompt | llm).invoke({
        "intro": intro.content,
        "strengths": strengths.content,
        "match": match.content
    })

    letter = f"""{intro.content.strip()}
        {strengths.content.strip()}
        {match.content.strip()}
        {closing.content.strip()}"""

    return letter
