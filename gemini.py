from dotenv import load_dotenv
import os
import csv
import json
from google import genai
from google.genai import types
import numpy as np
import generate

load_dotenv()
csv_file = csv.reader(open('skills.csv', 'r'), delimiter=',')

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(GEMINI_API_KEY)

def lookup_skill_misconceptions(skill_code: str) -> tuple[str, str]:
    """
    Lookup skill and misconceptions from the CSV file based on the skill code.

    Args:
        skill_code (str): The skill code to look up.
    """
    skill = ""
    misconceptions = ""
    for row in csv_file:
        if row[1] == skill_code:
            skill = row[3]
            misconceptions = row[5]
            break
    return skill, misconceptions

def generate_distractors_batch(questions_data: list[dict]) -> dict:
    """
    Generate distractors for a BATCH of questions.
    
    Args:
        questions_data: List of dicts, e.g., 
        [{'id': 1, 'question': '1+1', 'correct_ans': 2, 'skill_code': 'ADD01'}, ...]
    """
    
    client = genai.Client(api_key=GEMINI_API_KEY) # Replace with your key variable
    
    # 1. Pre-process data to include skills/misconceptions
    processed_inputs = []
    for q in questions_data:
        skill, misconceptions = lookup_skill_misconceptions(q['skill_code'])
        processed_inputs.append({
            "question": q['question'],
            "correct_ans": q['correct_ans'],
            "skill": skill,
            "misconceptions": misconceptions
        })

    # 2. Define the Schema for a LIST of results
    # We need an object that contains a list of objects
    batch_schema = {
        "type": "object",
        "properties": {
            "results": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "distractors": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "minItems": 3,
                            "maxItems": 3
                        }
                    },
                    "required": ["distractors"]
                }
            }
        },
        "required": ["results"]
    }

    # 3. Construct the Prompt
    prompt_text = (
        "Generate 3 distractors for each of the following questions based on the "
        "provided skill and common misconceptions.\n\n"
        f"Input Data: {json.dumps(processed_inputs)}"
    )

    # 4. Call the API
    response = client.models.generate_content(
        model="gemini-2.5-flash", # verified model name (adjust if you have 2.0 access)
        contents=[prompt_text],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=batch_schema,
            temperature=0.8,
            system_instruction="""You are an expert math distractor generator.
            For each item, use the question, correct answer, skill name, and misconceptions
            to propose 3 high-quality distractors.
            Return them strictly following the JSON schema."""
        )
    )

    # 5. Parse and Return
    try:
        result = json.loads(response.text)
        # Convert list back to a dict keyed by ID for easy lookup if needed
        # or just return the list
        return result['results'] 
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return []

# --- Usage Example ---

# questions_to_process = [
#     {"question": "5 + 3", "correct_ans": 8, "skill_code": "ADD_01"},
#     {"question": "10 - 4", "correct_ans": 6, "skill_code": "SUB_01"},
#     # ... add up to 20 questions here ...
# ]

# - - -

def generate_distractors(question: str, correct_ans: int, skill_code: str) -> list[int]:
    """
    Generate distractors for a given question and correct answer using Gemini API.

    Args:
        question (str): The question string.
        correct_ans (int): The correct answer to the question.
        skill_code (str): The skill code indicating the type of distractor generation.

    Returns:
        list[int]: A list of generated distractors.
    """

    client = genai.Client(api_key=GEMINI_API_KEY)

    # find skill, misconceptions from csv
    skill, misconceptions = lookup_skill_misconceptions(skill_code)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            f"Generate 3 distractors for the question: {question} with correct answer: {correct_ans} using skill: {skill}. Account for the following misconceptions: {misconceptions}"
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "required": [
                    "distractors"
                ],
                "properties": {
                    "distractors": {
                        "type": "array",
                        "items": {
                            "type": "integer"
                        },
                        "minItems": 3,
                        "maxItems": 3
                    }
                },
                "type": "object"
            },
            temperature=0.8,
            system_instruction="""You are an expert question generator specializing in creating plausible distractors for multiple-choice questions in mathematics.
            Given a question, its correct answer, the name of the skill/competency, and common misconceptions, you will provide 3 distractors for each question."""
        )
    )
    print(response.text)
    result = json.loads(response.text)
    return result['distractors']

def get_questions(skill_id: str, num_questions: int) -> list[dict]:
    skill, misconceptions = lookup_skill_misconceptions(skill_id)
    raw_questions = generate.gen_questions(skill_id, num_questions)
    questions = []
    for q in raw_questions:
        question, answer = q
        questions.append({
            "question": question,
            "correct_ans": answer,
            "skill_code": skill,
            "misconceptions": misconceptions
        })
    return questions

if __name__ == "__main__":

    # questions to process
    worksheet_questions = []
    worksheet_questions.extend(get_questions("1A", 5))
    worksheet_questions.extend(get_questions("2A1", 5))
    worksheet_questions.extend(get_questions("2S2", 5))
    worksheet_questions.extend(get_questions("T10", 5))

    # This uses only 1 API call for all questions
    batch_results = generate_distractors_batch(worksheet_questions)

    # for res in batch_results:
    #     print(f"Distractors: {res['distractors']}")

    for i, res in enumerate(batch_results):
        q = worksheet_questions[i]
        print(f"Q: {q['question']} | Ans: {q['correct_ans']} | Distractors: {res['distractors']}")