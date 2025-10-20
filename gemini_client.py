import os
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


# ====== MODEL CONFIG ======
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


# ====== HELPER FUNCTIES ======
def get_prompt_prefix(language: str, tone: str) -> str:
    """
    Return a language + tone specific prefix for each prompt.
    """
    lang = language.lower()
    tone = tone.lower()

    if lang.startswith("n"):
        return f"Schrijf in het Nederlands een motivatiebrief in een {tone} toon."
    return f"Write the motivation letter in English with a {tone} tone."


# ====== PROMPTS ======
intro_prompt = PromptTemplate.from_template("""
{prefix}

You are writing the introduction paragraph for a professional motivation letter.
It should sound personal, enthusiastic, and relevant.

User information:
{user_info}

Write only the introduction paragraph.
""")

strengths_prompt = PromptTemplate.from_template("""
{prefix}

Continue the motivation letter naturally after the introduction below.

Introduction:
{intro}

Now write a paragraph describing 2–3 of the user's key strengths, achievements, or professional qualities.
Keep the same tone and flow.

User information:
{user_info}
""")

match_prompt = PromptTemplate.from_template("""
{prefix}

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
{prefix}

You are finishing a motivation letter that currently contains the following paragraphs:

Introduction:
{intro}

Strengths:
{strengths}

Alignment:
{match}

Write a polite, optimistic closing paragraph that fits naturally with the rest of the letter.
""")


# ====== GENERATE FUNCTION ======
def generate_motivation_letter(
    user_info: str,
    job_description: str,
    language: str = "English",
    tone: str = "Formal"
) -> str:
    """
    Generate a motivation letter in a given language and tone.
    Supported languages: English, Dutch.
    Supported tones: Formal, Friendly, Enthusiastic, Confident, etc.
    """
    prefix = get_prompt_prefix(language, tone)

    # ---- Step 1: Introduction ----
    intro = (intro_prompt | llm).invoke({
        "prefix": prefix,
        "user_info": user_info
    })

    # ---- Step 2: Strengths ----
    strengths = (strengths_prompt | llm).invoke({
        "prefix": prefix,
        "intro": intro.content,
        "user_info": user_info
    })

    # ---- Step 3: Job Alignment ----
    match = (match_prompt | llm).invoke({
        "prefix": prefix,
        "intro": intro.content,
        "strengths": strengths.content,
        "user_info": user_info,
        "job_description": job_description
    })

    # ---- Step 4: Closing ----
    closing = (closing_prompt | llm).invoke({
        "prefix": prefix,
        "intro": intro.content,
        "strengths": strengths.content,
        "match": match.content
    })

    # ---- Combine everything ----
    letter = "\n\n".join([
        intro.content.strip(),
        strengths.content.strip(),
        match.content.strip(),
        closing.content.strip()
    ])

    return letter
