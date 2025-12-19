import csv
import json
from enum import Enum

def csv_to_json(csv_path, json_path):
    skills = []
    csv_file = csv.reader(open('skills.csv', 'r'), delimiter=',')
    next(csv_file)  # Skip header row

    for row in csv_file:
        code = row[1]
        name = row[3]
        diff = int(row[2])
        example = row[4]
        misconceptions = row[5]

        skills.append({
            "code": code.strip(),
            "name": name.strip(),
            "difficulty": diff,
            "example": example.strip(),
            "misconceptions": misconceptions.strip()
        })

    with open(json_path, "w", encoding="utf-8") as out:
        json.dump(skills, out, indent=2, ensure_ascii=False)

    return json_path

if __name__ == "__main__":
    csv_to_json("skills.csv", "skills.json")