import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv() #This will set the variables in .env as environment variables

class Chain:
    def __init__(self, api_key):
        self.llm = ChatGroq(
            model = 'llama-3.3-70b-versatile',
            groq_api_key = api_key,
            temperature=0,
        )
    
    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            SCRAPED TEXTS FROM WEBSITE:
            {page_data}
            ### INSTRUCTIONS:
            The scraped text is from careers tab of some website.
            Your job is to extract the job postings and return them in json format with the following keys:
            'role','experience','skills','description'
            For skills break the requirements into components and list only the core 3-5 skills.
            For description, include the company name, any specific company members name or terms used.
            NO PREAMBLE. No /n 
            Return in this format:
            {{
                "role":"",
                "experience":"",
                "skills":["","",etc],
                "description":"",
            }}
            """
        )

        chain_extract = prompt_extract | self.llm

        response = chain_extract.invoke({"page_data": cleaned_text})
        print("3333: ", response.content)

        try:
            res = JsonOutputParser().parse(str(response.content))
        except OutputParserException:
            raise OutputParserException("Context too big for json parse")
        
        if not(isinstance(res, dict)):
            print("RES IS NOT DICT. Its in format: ", type(res))
        return res
    
    def generate_email(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ###JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Asesh, a skilled developer studying in bachelors related to tech who has worked on many projects. 
            Your job is to write a cold email to the company regarding the job description mentioned above. Use specifics provided in the job description. Use terms used in the job description.
            Also add the most relevant ones from the following links as your portfolio:
            {links_list}
            [No PREAMBLE]
            ### Email [NO PREAMBLE]
        """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "links_list": links})
        return res.content