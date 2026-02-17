
def extract_skills_list(skills_text):
    if not skills_text:
        return []
    if isinstance(skills_text, list):
        return [s.replace('{{','').replace('}}','').strip() for s in skills_text if s.lower() not in ['skills', 'skill']]
    if ':' in skills_text:
        skills_text = skills_text.split(':', 1)[1]
    skills = [s.strip() for s in skills_text.split(',') if s.strip()]
    return [s.replace('{{','').replace('}}','').strip() for s in skills if s.lower() not in ['skills', 'skill']]

def calculate_skills_match(resume_skills, job_skills_text):
    job_skills_list = extract_skills_list(job_skills_text)
    missing_skills = job_skills_list # Simplified for test
    final_missing = []
    for skill in missing_skills:
        clean = skill.replace('{', '').replace('}', '').strip()
        if clean.lower() not in ['skill', 'skills', '']:
            final_missing.append(skill)
    return final_missing

test_input = "{{ skill }}, java, python, {{ skill }}"
print(f"Input: {test_input}")
print(f"Result: {calculate_skills_match([], test_input)}")

test_input_2 = "html, css, javascript, java"
print(f"Input 2: {test_input_2}")
print(f"Result 2: {calculate_skills_match([], test_input_2)}")
