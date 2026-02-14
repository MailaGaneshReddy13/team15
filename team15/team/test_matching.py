def extract_skills_list(skills_text):
    """Helper to extract list of skills from comma-separated string."""
    if not skills_text:
        return []
    return [s.strip() for s in skills_text.split(',') if s.strip()]

def calculate_skills_match(resume_skills, job_skills_text):
    """
    Calculates matched and missing skills dynamically.
    resume_skills: list of strings
    job_skills_text: comma-separated string
    """
    # Normalize job skills (lowercase for comparison)
    job_skills_list = extract_skills_list(job_skills_text)
    job_skills_set = set(s.lower() for s in job_skills_list)
    
    # Normalize resume skills
    if isinstance(resume_skills, str):
        # Handle case where resume_skills might be a string
        resume_skills = extract_skills_list(resume_skills)
    
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

# Test Case
resume_skills = ["Python", "SQL"]
job_skills = "Python, Django, SQL, Docker"

matched, missing = calculate_skills_match(resume_skills, job_skills)

print(f"Resume: {resume_skills}")
print(f"Job: {job_skills}")
print(f"Matched: {matched}")
print(f"Missing: {missing}")

expected_matched = ["Python", "SQL"]
expected_missing = ["Django", "Docker"]

assert set(matched) == set(expected_matched)
assert set(missing) == set(expected_missing)

print("Test Passed!")
