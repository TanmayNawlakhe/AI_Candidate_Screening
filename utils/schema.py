SCHEMA_DESCRIPTION = """
The 'candidates' table schema is as follows (ignore job_position_name, educational_requirements, experience_requirement, age_requirement, responsibilities_job, and skills_required columns):

- candidate_id: Auto-generated primary key.
- name: Full name of the candidate.
- address: Candidate's address.
- career_objective: Career goals.
- skills: List of skills (JSON array).
- educational_institution_name: List of institutions attended (JSON array).
- degree_names: Degrees earned (JSON array).
- passing_years: Passing years of education (JSON array).
- educational_results: Education results (JSON array).
- result_types: Types of educational results (JSON array).
- major_field_of_studies: Major fields of study (JSON array).
- professional_company_names: Previous employers (JSON array).
- company_urls: URLs of company profiles (JSON array).
- start_dates: Start dates for jobs (JSON array).
- end_dates: End dates for jobs (JSON array).
- yoe: Years of experience (number).
- related_skills_in_job: Related skills mentioned in job descriptions (JSON array).
- positions: Positions held (JSON array).
- locations: Job locations (JSON array).
- responsibilities: Job responsibilities (string).
- extra_curricular_activity_types: Types of extracurricular activities (JSON array).
- extra_curricular_organization_names: Names of organizations (JSON array).
- extra_curricular_organization_links: URLs of organization profiles (JSON array).
- role_positions: Roles in organizations (JSON array).
- languages: Languages spoken (JSON array).
- proficiency_levels: Language proficiency levels (JSON array).
- certification_providers: Certification providers (JSON array).
- certification_skills: Certified skills (JSON array).
- online_links: Links to personal profiles (JSON array).
- issue_dates: Certification issue dates (JSON array).
- expiry_dates: Certification expiry dates (JSON array).
"""
