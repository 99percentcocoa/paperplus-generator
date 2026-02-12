"""
Create a 20-question worksheet with questions and distractors.
Saves the worksheet to a JSON file.
"""

import json
import random
import generate
import distractors
from utils import number_to_letter


def create_worksheet(skill_distribution: dict = None) -> list:
    """
    Create a 20-question worksheet with questions and distractors.
    
    Args:
        skill_distribution: Dict mapping skill_code to number of questions.
                           If None, uses a default distribution.
    
    Returns:
        List of Question objects with chosen distractors.
    """
    
    # Default distribution if not provided
    if skill_distribution is None:
        skill_distribution = {
            "1A": 2,
            "2A1": 3,
            "2A2": 2,
            "2S1": 2,
            "T5": 2,
            "T10": 2,
            "3A": 2,
            "3S": 2,
            "2M1": 1,
            "2D1": 0,
        }
    
    # Verify total is 20
    total = sum(skill_distribution.values())
    if total != 20:
        raise ValueError(f"Skill distribution must sum to 20, got {total}")
    
    worksheet = []
    
    for skill_code, num_questions in skill_distribution.items():
        # Generate raw questions
        raw_questions = generate.gen_questions(skill_code, num_questions)
        
        for question_text, correct_ans in raw_questions:
            # Generate possible distractors
            try:
                possible_distractors = distractors.generate_distractors(
                    skill_code, question_text, correct_ans
                )
            except Exception as e:
                print(f"Error generating distractors for {skill_code}: {e}")
                possible_distractors = []
            
            # Ensure we have enough distractors
            if len(possible_distractors) < 3:
                # Fallback: generate generic offsets
                for offset in [-2, -1, 1, 2]:
                    possible_distractors.append(int(correct_ans) + offset)
                possible_distractors = list(set(possible_distractors))
                # Remove correct answer and ensure we have 3+
                possible_distractors = [d for d in possible_distractors if d != correct_ans][:3]
            
            # Create Question object
            question = generate.Question(
                question_text=question_text,
                skill_code=skill_code,
                options=[correct_ans],  # Will be replaced by choose_distractors
                answer=1,  # Will be updated by choose_distractors
                possible_distractors=possible_distractors
            )
            
            # Choose distractors and randomize positions
            question.choose_distractors()
            
            # Convert answer from 1-4 to A-D
            question.answer = number_to_letter(question.answer)
            
            worksheet.append(question)
    
    return worksheet


def worksheet_to_json(worksheet: list) -> list:
    """
    Convert worksheet to JSON-serializable format matching example_worksheet.json template.
    
    Args:
        worksheet: List of Question objects
    
    Returns:
        List with [{"answerKey": [...]}, [...questions...]]
    """
    questions = []
    answer_key = []
    
    for q in worksheet:
        # answer is already a letter (A-D) from create_worksheet
        answer_letter = q.answer
        
        questions.append({
            "question_text": q.question_text,
            "skill_code": q.skill_code,
            "options": [str(opt) for opt in q.options],
            "correct_option": answer_letter
        })
        answer_key.append(answer_letter)
    
    return [
        {"answerKey": answer_key},
        questions
    ]


def save_worksheet(worksheet_data: list, filename: str = "worksheet.json"):
    """
    Save worksheet data to JSON file.
    
    Args:
        worksheet_data: List with [{"answerKey": [...]}, [...questions...]]
        filename: Output filename
    """
    with open(filename, "w") as f:
        json.dump(worksheet_data, f, indent=2)
    print(f"Worksheet saved to {filename}")


if __name__ == "__main__":
    print("Creating 20-question worksheet...")
    
    # Create worksheet with custom distribution (optional)
    custom_distribution = {
        "1A": 3,
        "1S": 2,
        "2A1": 3,
        "2A2": 2,
        "2S1": 2,
        "2S2": 2,
        "T5": 2,
        "T10": 1,
        "3A": 1,
        "3S": 1,
        "2M1": 1,
    }
    
    worksheet = create_worksheet(custom_distribution)
    print(f"Created {len(worksheet)} questions")
    
    # Convert to JSON format
    worksheet_json = worksheet_to_json(worksheet)
    
    # Save to file
    save_worksheet(worksheet_json, "worksheet.json")
    
    # Also print a preview
    print("\n--- Worksheet Preview ---")
    questions = worksheet_json[1]  # Questions are in the second element
    for q in questions[:3]:
        print(f"\n{q['question_text']}")
        for i, opt in enumerate(q['options']):
            print(f"   {chr(65 + i)}) {opt}")
    print(f"\n... and {len(questions) - 3} more questions")
