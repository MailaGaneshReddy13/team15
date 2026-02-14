
def extract_skills_list(skills_text):
    """Helper to extract list of skills from comma-separated string."""
    if not skills_text:
        return []
    if isinstance(skills_text, list):
        return skills_text
    return [s.strip() for s in skills_text.split(',') if s.strip()]

def calculate_skills_match(resume_skills, job_skills_text):
    print(f"DEBUG: Resume Skills Input: {resume_skills} (Type: {type(resume_skills)})")
    
    # Normalize job skills (lowercase for comparison)
    job_skills_list = extract_skills_list(job_skills_text)
    job_skills_set = set(s.lower() for s in job_skills_list)
    
    # Normalize resume skills
    if isinstance(resume_skills, str):
        # Handle case where resume_skills might be a string
        resume_skills = extract_skills_list(resume_skills)
    
    print(f"DEBUG: Resume Skills List: {resume_skills}")
    
    resume_skills_set = set(s.lower() for s in resume_skills)

    # Calculate matches (intersection)
    matched_skills_lower = job_skills_set.intersection(resume_skills_set)
    missing_skills_lower = job_skills_set.difference(resume_skills_set)
    
    # Re-map to original cases for display niceness
    matched_skills = []
    missing_skills = []
    
    # Map back to original job skill casing
    for skill in job_skills_list:
        if skill.lower() in matched_skills_lower:
            matched_skills.append(skill)
        elif skill.lower() in missing_skills_lower:
            missing_skills.append(skill)
            
    return matched_skills, missing_skills

# Test Case 1: Resume skills as list
r_skills = ["Python", "Django", "SQL"]
j_skills = "Python, Django, AWS, React"
matched, missing = calculate_skills_match(r_skills, j_skills)
print(f"Matched: {matched}")
print(f"Missing: {missing}")

# Test Case 2: Resume skills as string
r_skills_str = "Python, Django, SQL"
matched, missing = calculate_skills_match(r_skills_str, j_skills)
print(f"Matched (Str): {matched}")
print(f"Missing (Str): {missing}")
