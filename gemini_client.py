from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


def generate_motivation_letter(user_info: str, job_description: str, language: str = "English", tone: str = "Formal") -> str:
    prompt = f"""
    Write a professional motivation letter based on the following information:

    User Information:
    {user_info}

    Job Description:
    {job_description}

    Language: {language}
    Tone: {tone}

    The letter should be professional, persuasive, and convincing.
    """

    message = HumanMessage(content=prompt)
    response = llm.invoke([message])

    return response.content
