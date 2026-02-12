import json
from pathlib import Path

# Cache for skills data
_skills_cache = None


def _load_skills():
    """Load skills data from skills.json file."""
    global _skills_cache
    if _skills_cache is not None:
        return _skills_cache
    
    skills_file = Path(__file__).parent / "skills.json"
    
    try:
        with open(skills_file, 'r') as f:
            data = json.load(f)
            # If data is a list, assume it's [{"answerKey": [...]}, [...skills...]]
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                # Check if first element has answerKey (old format)
                if "answerKey" in data[0]:
                    _skills_cache = {}
                else:
                    # It's a list of skill objects
                    _skills_cache = {skill["code"]: skill for skill in data}
            else:
                # It's a dict or list of skills
                _skills_cache = {skill["code"]: skill for skill in data}
            return _skills_cache
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get_difficulty_level(skill_code):
    """
    Get the difficulty level for a given skill code.
    
    Args:
        skill_code: str representing the skill code (e.g., "1A", "2M1")
    
    Returns:
        int or str: The difficulty level, or None if skill code not found
    
    Raises:
        ValueError: If skill code is not found in skills.json
    """
    skills = _load_skills()
    
    if skill_code not in skills:
        raise ValueError(f"Skill code '{skill_code}' not found in skills.json")
    
    difficulty = skills[skill_code].get("difficulty_level")
    # Convert to int if it's a string
    if isinstance(difficulty, str):
        try:
            return int(difficulty)
        except ValueError:
            return difficulty
    return difficulty


def number_to_letter(num):
    """
    Convert numeric answer (1, 2, 3, 4) to letter (A, B, C, D).
    
    Args:
        num: int or str representing the answer position (1-4)
    
    Returns:
        str: The corresponding letter (A, B, C, or D)
    
    Raises:
        ValueError: If input is not 1-4
    """
    # Convert to int if string
    if isinstance(num, str):
        try:
            num = int(num)
        except ValueError:
            raise ValueError(f"Invalid input: {num}. Must be '1', '2', '3', or '4'")
    
    # Map number to letter
    mapping = {1: "A", 2: "B", 3: "C", 4: "D"}
    
    if num not in mapping:
        raise ValueError(f"Invalid answer number: {num}. Must be 1, 2, 3, or 4")
    
    return mapping[num]


def letter_to_index(letter):
    """
    Convert letter answer (A, B, C, D) to index (0, 1, 2, 3).
    
    Args:
        letter: str representing the answer letter (A-D, case-insensitive)
    
    Returns:
        int: The corresponding index (0, 1, 2, or 3)
    
    Raises:
        ValueError: If input is not A-D
    """
    # Convert to uppercase if needed
    if isinstance(letter, str):
        letter = letter.upper()
    else:
        raise ValueError(f"Invalid input type: {type(letter)}. Must be a string")
    
    # Map letter to index
    mapping = {"A": 0, "B": 1, "C": 2, "D": 3}
    
    if letter not in mapping:
        raise ValueError(f"Invalid answer letter: {letter}. Must be A, B, C, or D")
    
    return mapping[letter]
