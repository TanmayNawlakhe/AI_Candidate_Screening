import cx_Oracle
import pandas as pd
import json
import re
from datetime import datetime
from config import DB_USER, DB_PASS, DB_DSN
from utils.lists import NAMES
from utils.lists import InsertionString


def safe_get_field(row, field_name):
    """Safely get field value with multiple possible field names"""
    possible_names = [field_name, field_name.lower(), field_name.upper()]
    for name in possible_names:
        if name in row and not pd.isnull(row[name]):
            return row[name]
    return None

def clean_special_chars(text):
    """Remove special characters that might cause issues"""
    if isinstance(text, str):
        # Replace common problematic characters
        text = text.replace('â€¢', '•').replace('â€"', '-').replace('â€™', "'")
        # Remove or replace other problematic unicode characters
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII characters
    return text

def calculate_total_yoe(start_dates_json, end_dates_json):
    try:
        start_dates = json.loads(start_dates_json)
        end_dates = json.loads(end_dates_json)
        total_months = 0

        for i in range(min(len(start_dates), len(end_dates))):
            start = str(start_dates[i]).replace('[','').replace(']','').replace("'", "").strip()
            end = str(end_dates[i]).replace('[','').replace(']','').replace("'", "").strip()

            if 'current' in end.lower():
                end = datetime.today().strftime('%b %Y')

            try:
                # Handle different date formats
                if len(start.split()) == 2:  # "May 2021"
                    start_dt = datetime.strptime(start, '%b %Y')
                else:  # Try other formats or default
                    start_dt = datetime.strptime(start, '%B %Y')
                
                if len(end.split()) == 2:  # "May 2021"
                    end_dt = datetime.strptime(end, '%b %Y')
                else:
                    end_dt = datetime.strptime(end, '%B %Y')

                delta = (end_dt.year - start_dt.year) * 12 + (end_dt.month - start_dt.month)
                total_months += max(delta, 0)
            except:
                continue  # Skip problematic dates

        return round(total_months / 12, 2)

    except Exception as e:
        print(f"Error calculating YOE: {e}")
        return 0

def process_field(row, field_name):
    """Improved field processing with better error handling"""
    field_value = safe_get_field(row, field_name)
    
    if pd.isnull(field_value) or field_value in ['None', '[None]', 'N/A', '', 'nan']:
        return json.dumps([])
    
    field_value = clean_special_chars(str(field_value))
    
    # Handle already valid JSON
    if isinstance(field_value, str) and field_value.strip().startswith('[') and field_value.strip().endswith(']'):
        try:
            # Try to parse as JSON first
            parsed = json.loads(field_value)
            return json.dumps(parsed)
        except json.JSONDecodeError:
            try:
                # Try eval as fallback
                parsed = eval(field_value)
                return json.dumps(parsed)
            except:
                # If both fail, treat as single item
                return json.dumps([field_value])
    
    # Handle nested lists like your related_skills_in_job
    if isinstance(field_value, str) and '[[' in field_value:
        try:
            parsed = eval(field_value)
            return json.dumps(parsed)
        except:
            return json.dumps([field_value])
    return json.dumps([field_value])

def preprocess_and_insert(csv_path):
    df = pd.read_csv(csv_path)
    connection = cx_Oracle.connect(DB_USER, DB_PASS, DB_DSN)
    cursor = connection.cursor()

    print(f"Processing {len(df)} records...")
    print("Columns in CSV:", df.columns.tolist())

    for index, row in df.iterrows():
        try:
            name = NAMES[index] if index < len(NAMES) else f"Candidate {index+1}"
            
            address = clean_special_chars(str(row.iloc[0])) if len(row) > 0 else 'N/A'
            career_objective = clean_special_chars(str(row.iloc[1])) if len(row) > 1 else 'N/A'

            # Process dates for YOE calculation
            start_dates = process_field(row, 'start_dates')
            end_dates = process_field(row, 'end_dates')
            yoe = calculate_total_yoe(start_dates, end_dates)

            # Insert in OracleDB
            cursor.execute({InsertionString}, {
                'name': name,
                'address': address[:500],
                'career_objective': career_objective,
                'skills': process_field(row, 'skills'),
                'edu_inst_names': process_field(row, 'educational_institution_names'),
                'degrees': process_field(row, 'degree_names'),
                'passing_years': process_field(row, 'passing_years'),
                'edu_results': process_field(row, 'educational_results'),
                'result_types': process_field(row, 'result_types'),
                'majors': process_field(row, 'major_field_of_studies'),
                'prof_companies': process_field(row, 'professional_company_names'),
                'comp_urls': process_field(row, 'company_urls'),
                'start_dates': start_dates,
                'end_dates': end_dates,
                'yoe': yoe,
                'related_skills': process_field(row, 'related_skills_in_job'),
                'positions': process_field(row, 'positions'),
                'locations': process_field(row, 'locations'),
                'responsibilities': clean_special_chars(safe_get_field(row, 'responsibilities') or 'N/A'),
                'extra_curr_types': process_field(row, 'extra_curricular_activity_types'),
                'extra_curr_org_names': process_field(row, 'extra_curricular_organization_names'),
                'extra_curr_org_links': process_field(row, 'extra_curricular_organization_links'),
                'role_positions': process_field(row, 'role_positions'),
                'languages': process_field(row, 'languages'),
                'proficiency_levels': process_field(row, 'proficiency_levels'),
                'cert_providers': process_field(row, 'certification_providers'),
                'cert_skills': process_field(row, 'certification_skills'),
                'online_links': process_field(row, 'online_links'),
                'issue_dates': process_field(row, 'issue_dates'),
                'expiry_dates': process_field(row, 'expiry_dates'),
                'job_position_name': clean_special_chars(safe_get_field(row, 'job_position_name') or 'N/A'),
                'educational_requirements': clean_special_chars(safe_get_field(row, 'educational_requirements') or 'N/A'),
                'experience_requirement': clean_special_chars(safe_get_field(row, 'experience_requirement') or 'N/A'),
                'age_requirement': clean_special_chars(safe_get_field(row, 'age_requirement') or 'N/A'),
                'responsibilities_job': clean_special_chars(safe_get_field(row, 'responsibilities_job') or 'N/A'),
                'skills_required': clean_special_chars(safe_get_field(row, 'skills_required') or 'N/A')
            })
            
            if index % 10 == 0:
                print(f"Processed {index + 1} records...")
                
        except Exception as e:
            print(f"Error processing record {index}: {e}")
            print(f"Row data: {row.to_dict()}")
            continue

    connection.commit()
    cursor.close()
    connection.close()
    print("Data insertion completed.")


if __name__ == '__main__':
    preprocess_and_insert('data/resume_data.csv')