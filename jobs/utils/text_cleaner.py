import re

def extract_data(input_string: str) -> list[str]:
    pattern = r"\d+\.\s([^\d]+?)(?=\d+\.|$)"
    activities = re.findall(pattern, input_string, re.DOTALL)
    return [activity.strip() for activity in activities]