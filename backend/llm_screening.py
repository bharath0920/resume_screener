import os
from dotenv import load_dotenv
import openai
import json

load_dotenv()

AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def try_parse_json(text):
    try:
        return json.loads(text)
    except Exception:
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end])
            except Exception:
                pass
        import ast
        try:
            return ast.literal_eval(text[start:end])
        except Exception:
            return None

def screen_resume_with_llm(job_description, resume_info):
    resume_text = resume_info['raw_text']
    name = resume_info.get('name')
    email = resume_info.get('email')
    filename = resume_info.get('filename', None)
    prompt = f"""
You are a strict technical resume screener, acting as a member of the hiring technology team (not HR). Given the following job description and candidate resume, analyze the candidate's fit for the role.

Job Description:
{job_description}

Candidate Resume:
{resume_text}

Instructions:
- Always refer to the applicant as 'the candidate' (never use he/she or their name).
- Screen the entire resume, not just highlights.
- Extract each technical qualification or requirement from the provided job description payload. For each, explicitly state in the summary and/or reason whether it is met, not met, or unclear, in the same order as the job description.
- If one or two qualifications are missing but the candidate is otherwise strong, highlight which are missing and factor this into the eligibility decision. Clearly mention which qualifications are missing and whether the candidate is still eligible or not based on the overall fit.
- For education, if the candidate meets the qualification, simply state 'the candidate meets the education qualification' and do not mention specific degrees or repeat education details. If not met, state which education qualification is missing.
- Consider an MCA as a master's degree in Computer Applications or a related field for the purpose of education qualification. Do not list the master's as missing if the candidate has an MCA and it is relevant.
- Use neutral, evidence-based language such as 'the candidate seems to...', 'the candidate appears to...', or 'the candidate demonstrates...'.
- Be strict and detail-oriented in your technical assessment, focusing on depth, relevance, and explicit evidence of technical skills and experience.
- Summarize the candidate's fit in one short sentence (max 25 words), suitable for a manager who does not want to read long passages. In the summary and reason, mention if technical qualifications are met and highlight other high-level strengths or gaps.
- Give a one-line reason (max 25 words) for your decision, listing any missing qualifications if applicable, and emphasizing technical fit if true.
- Decide if the candidate is eligible for the position (true/false). If eligible, simply state that the candidate meets the eligibility criteria.
- Output a single JSON object with keys: summary, eligible (true/false), reason.
- Do not include any explanation or text outside the JSON object.
"""
    try:
        if AZURE_OPENAI_KEY and AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT:
            client = openai.AzureOpenAI(
                api_key=AZURE_OPENAI_KEY,
                api_version=AZURE_OPENAI_API_VERSION,
                azure_endpoint=AZURE_OPENAI_ENDPOINT,
            )
            response = client.chat.completions.create(
                model=AZURE_OPENAI_DEPLOYMENT,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=700,
                temperature=0.2
            )
        else:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=700,
                temperature=0.2
            )
        text = response.choices[0].message.content
        result = try_parse_json(text)
        if not result:
            return {
                "filename": filename,
                "name": name,
                "email": email,
                "summary": None,
                "eligible": False,
                "reason": "LLM screening failed: Could not parse LLM output as JSON."
            }
        if filename:
            result['filename'] = filename
        if name:
            result['name'] = name
        if email:
            result['email'] = email
        return result
    except Exception as e:
        return {
            "filename": filename,
            "name": name,
            "email": email,
            "summary": None,
            "eligible": False,
            "reason": f"LLM screening failed: {str(e)}"
        } 