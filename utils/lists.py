NAMES = [
    'Alice Smith', 'Bob Johnson', 'Carol Lee', 'David Brown', 'Eva Adams',
    'Frank Miller', 'Grace Wilson', 'Henry Davis', 'Ivy Taylor', 'Jack Anderson',
    'Kate Martinez', 'Liam Garcia', 'Maya Rodriguez', 'Noah Thompson', 'Olivia White',
    'Peter Harris', 'Quinn Clark', 'Rachel Lewis', 'Sam Walker', 'Tina Hall',
    'Uma Allen', 'Victor Young', 'Wendy King', 'Xavier Wright', 'Yara Lopez',
    'Zoe Hill', 'Aaron Green', 'Bella Adams', 'Carlos Nelson', 'Diana Carter',
    'Ethan Mitchell', 'Fiona Perez', 'George Roberts', 'Hannah Turner', 'Ian Phillips',
    'Julia Campbell', 'Kevin Parker', 'Luna Evans', 'Marcus Edwards', 'Nina Collins',
    'Oscar Stewart', 'Penny Sanchez', 'Quincy Morris', 'Ruby Reed', 'Seth Cook',
    'Tara Bailey', 'Ulysses Rivera', 'Vera Cooper', 'Wade Richardson', 'Xara Cox',
    'Yasmin Ward', 'Zachary Torres', 'Aria Peterson', 'Blake Gray', 'Chloe Ramirez',
    'Drake James', 'Elena Watson', 'Felix Brooks', 'Gina Kelly', 'Hugo Sanders',
    'Iris Price', 'Jasper Bennett', 'Kira Wood', 'Leo Barnes', 'Mia Ross',
    'Nolan Henderson', 'Opal Coleman', 'Paulo Jenkins', 'Quinlan Perry', 'Rosa Powell',
    'Silas Long', 'Thea Patterson', 'Uriel Hughes', 'Violet Flores', 'Wesley Butler',
    'Ximena Simmons', 'Yorick Foster', 'Zelda Gonzales', 'Axel Bryant', 'Brynn Alexander',
    'Cyrus Russell', 'Delilah Griffin', 'Emilio Diaz', 'Freya Hayes', 'Gideon Myers',
    'Hazel Ford', 'Ignacio Hamilton', 'Jessa Graham', 'Knox Sullivan', 'Lydia Wallace',
    'Mateo Woods', 'Nora Fisher', 'Owen Murray', 'Piper Webb', 'Quinton McDonald',
    'Reese Bell', 'Sofia Stone', 'Tobias Palmer', 'Unity Robertson', 'Vincent Cruz',
    'Willa Spencer', 'Xander Marshall'
]

InsertionString = """INSERT INTO candidates (
                    name, address, career_objective, skills, educational_institution_name, degree_names,
                    passing_years, educational_results, result_types, major_field_of_studies,
                    professional_company_names, company_urls, start_dates, end_dates, yoe,
                    related_skills_in_job, positions, locations, responsibilities,
                    extra_curricular_activity_types, extra_curricular_organization_names,
                    extra_curricular_organization_links, role_positions, languages,
                    proficiency_levels, certification_providers, certification_skills,
                    online_links, issue_dates, expiry_dates, job_position_name,
                    educational_requirements, experience_requirement, age_requirement,
                    responsibilities_job, skills_required
                ) VALUES (
                    :name, :address, :career_objective, :skills, :edu_inst_names, :degrees,
                    :passing_years, :edu_results, :result_types, :majors,
                    :prof_companies, :comp_urls, :start_dates, :end_dates, :yoe,
                    :related_skills, :positions, :locations, :responsibilities,
                    :extra_curr_types, :extra_curr_org_names,
                    :extra_curr_org_links, :role_positions, :languages,
                    :proficiency_levels, :cert_providers, :cert_skills,
                    :online_links, :issue_dates, :expiry_dates, :job_position_name,
                    :educational_requirements, :experience_requirement, :age_requirement,
                    :responsibilities_job, :skills_required
                )"""

keywords = ["candidate","person", "student", "knowledge","expertise","expert","internship", "intern", "experience", "skills", "degree", "job", "employment", "position", "yoe", "detail", "details","education"]