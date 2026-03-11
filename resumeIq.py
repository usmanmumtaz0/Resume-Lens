import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

os.environ["GOOGLE_API_KEY"] = ""

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")


template = """
Extract the following information from the resume.

1 Name
2 Address
3 Contact
4 List of Projects

Give output in exactly 4 lines like this:

Name:
Address:
Contact:
Projects:

Resume:
{resume}
"""

prompt = PromptTemplate(
    input_variables=["resume"],
    template=template
)

parser = StrOutputParser()

chain = prompt | llm | parser

resume_text = """
Curriculum Vitae

Personal Information
My name is Omer Osman. I am a passionate Computer Science student who enjoys building software and learning modern technologies related to artificial intelligence and web development.

Address
House 27, Street 10, Johar Town, Lahore, Pakistan.

Contact Information
Phone Number: +92 300 1234567
Email: omer.osman@email.com
LinkedIn: linkedin.com/in/omer-osman

Objective
To obtain a challenging position in a software development or artificial intelligence role where I can apply my programming knowledge, improve my technical skills, and contribute to innovative projects.

Education
Bachelor of Science in Computer Science
Lahore Garrison University
Expected Graduation: 2026

Relevant Coursework
Data Structures and Algorithms, Operating Systems, Database Systems, Artificial Intelligence, Machine Learning, Software Engineering.

Technical Skills
Programming Languages: Python, C++, JavaScript
Frameworks: FastAPI, Next.js
Tools: Git, GitHub, Docker
Libraries: LangChain, NumPy, Pandas

Projects

AI Email Tone Converter
Developed a tool using Python and LangChain that converts email messages into different tones such as professional, friendly, or formal using large language models.

Stock Monitoring System
Built a stock monitoring application that tracks product inventory, generates alerts when stock is low, and provides reporting functionality for business users.

LangChain Chatbot
Designed and implemented a chatbot using LangChain and Gemini API that can answer user queries and perform prompt-based tasks.

Personal Portfolio Website
Created a responsive portfolio website using Next.js to showcase projects, technical skills, and achievements.

Experience
Worked on multiple university assignments involving algorithm design, data structures, and backend development using Python.

Achievements
Participated in programming competitions and hackathons at university level.

Interests
Artificial Intelligence, Machine Learning, Backend Development, and building automation tools.
"""

result = chain.invoke({
    "resume": resume_text
})


print(result)
