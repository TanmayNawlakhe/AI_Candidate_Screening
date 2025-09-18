# AI Resume Screening System - Complete Setup Guide

## 📋 Project Overview
An AI-powered candidate screening system that converts natural language queries into SQL and provides intelligent responses using Google's Gemini AI and Oracle Database.

## 🎯 Features
- Natural language to SQL query conversion
- Intelligent candidate search and filtering
- Experience calculation and skills matching
- Chat-based interface using Streamlit

---

## 📦 Prerequisites Installation Guide

### Step 1: Install Python (3.8 or higher)
1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, **CHECK** "Add Python to PATH"
3. Verify installation:
   ```bash
   python --version
   pip --version
   ```

### Step 2: Install Oracle Instant Client (FIRST!)
1. **Download Instant Client:**
   - Visit: https://www.oracle.com/database/technologies/instant-client/downloads.html
   - Select your OS (Windows x64)
   - Download "Basic Package" (Version 23.x)
   - File will be named something like: `instantclient-basic-windows.x64-23.x.x.x.zip`

2. **Extract and Configure:**
   ```bash
   # RIGHT-CLICK on the zip file and "Extract All" or use WinRAR/7-Zip
   # Extract to C:\oracle (Run as Administrator if needed)
   # This will automatically create: C:\oracle\instantclient_23_9
   # (version number may vary like instantclient_23_9 or instantclient_23_5)
   
   # Add to System PATH:
   # 1. Press Win + X, select "System"
   # 2. Click "Advanced system settings"
   # 3. Click "Environment Variables"
   # 4. Under "System variables", find and select "Path", click "Edit"
   # 5. Click "New" and add: C:\oracle\instantclient_23_9
   # 6. Click "OK" on all windows
   ```

### Step 3: Install Oracle Database 23ai Free
1. **Download Oracle Database 23ai Free:**
   - Visit: https://www.oracle.com/database/free/
   - Click "Download Oracle Database Free"
   - Choose "Windows x64" (or your OS)

2. **Install Oracle Database:**
   - **IMPORTANT: RIGHT-CLICK on setup.exe and select "Run as administrator"**
   - Choose "Single Instance database installation"
   - Select "Desktop class"
   - Oracle base: `C:\app\oracle`
   - Database edition: "Oracle Database 23ai Free"
   - Character set: "Use Unicode (AL32UTF8)"
   - If asked for user: Enter SYSTEM.
     - Remeber Passwords entered.

   - Global database name: `FREE`
   - Pluggable database name: `FREEPDB1`
   - Note the following defaults:
     - Port: `1521`
     - Service Name: `FREEPDB1`
   
3. **Verify Database Installation:**
   ```bash
   # Check if Oracle service is running (Windows)
   sc query OracleServiceFREE
   
   # Should show STATE: RUNNING
   # If not running:
   net start OracleServiceFREE
   ```

4. **Test Database Connection:**
   ```bash
   # Open Command Prompt and test with sqlplus
   sqlplus system/YourPassword123#@localhost:1521/FREEPDB1
   
   # If connected, you'll see: Connected to: Oracle Database 23ai Free...
   # Type 'exit' to quit sqlplus
   ```

### Step 4: Install SQL Developer (Optional but Recommended)
1. **Download SQL Developer:**
   - Visit: https://www.oracle.com/database/sqldeveloper/
   - Download the Windows 64-bit with JDK included
   - Extract to a folder like `C:\sqldeveloper`

2. **Run SQL Developer:**
   - Navigate to extracted folder
   - **RIGHT-CLICK on `sqldeveloper.exe` and select "Run as administrator"**

3. **Create Database Connection:**
   - Click the green "+" icon for new connection
   - Fill in:
     - Connection Name: `local_resume_db`
     - Username: `SYSTEM`
     - Password: `YourPassword123#` #Your defined password during oracledb setup
     - Save Password: ✓ (check)
     - Hostname: `localhost`
     - Port: `1521`
     - Service name: `FREEPDB1` (select radio button)
   - Click "Test" - should show "Status: Success"
   - Click "Save" then "Connect"

---

## 🚀 Project Setup

### Step 1: Clone/Download the Repository
```bash
# Using git
git clone https://github.com/TanmayNawlakhe/AI_Candidate_Screening.git
cd AI-Candidate-Screening

```

### Step 2: Update Configuration

**Edit `config.py`:**
```python
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
DB_USER = "SYSTEM"
DB_PASS = "oracledb"
DB_DSN = "localhost:1521/FREEPDB1"

```

### Step 3: Get Gemini API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the generated key
5. Replace `YOUR_GEMINI_API_KEY` in `config.py` with your actual key

### Step 4: Install Python Dependencies
```bash
# Open Command Prompt in project directory

# Install all required packages
pip install -r requirements.txt
```


## 🏃‍♂️ Running the Application

### Step 1: Verify Oracle Service is Running
```bash
# Windows Command Prompt (Run as Administrator)
net start OracleServiceFREE

# If already running, you'll see:
# "The requested service has already been started."
```

### Step 2: Setup Database Schema
```bash
# Paste and execute below query in SQL Developer worksheet:
CREATE TABLE candidates (
    candidate_id NUMBER GENERATED ALWAYS AS IDENTITY
        START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE NOT NULL,
    name VARCHAR2(200 BYTE),
    address VARCHAR2(500 BYTE),
    career_objective CLOB,
    skills CLOB,
    educational_institution_name CLOB,
    degree_names CLOB,
    passing_years CLOB,
    educational_results CLOB,
    result_types CLOB,
    major_field_of_studies CLOB,
    professional_company_names CLOB,
    company_urls CLOB,
    start_dates CLOB,
    end_dates CLOB,
    yoe NUMBER,
    related_skills_in_job CLOB,
    positions CLOB,
    locations CLOB,
    responsibilities CLOB,
    extra_curricular_activity_types CLOB,
    extra_curricular_organization_names CLOB,
    extra_curricular_organization_links CLOB,
    role_positions CLOB,
    languages CLOB,
    proficiency_levels CLOB,
    certification_providers CLOB,
    certification_skills CLOB,
    online_links CLOB,
    issue_dates CLOB,
    expiry_dates CLOB,
    job_position_name VARCHAR2(200 BYTE),
    educational_requirements CLOB,
    experience_requirement VARCHAR2(200 BYTE),
    age_requirement VARCHAR2(100 BYTE),
    responsibilities_job CLOB,
    skills_required CLOB
);
# Should output:
# ✅ Database setup completed successfully!
```

### Step 3: Load Sample Data
```bash
# Ensure you have resume_data.csv in the data/ folder
python -m backend.db_setup

# This will process and insert all resume data
# May take a few minutes depending on data size
```

### Step 4: Run the Streamlit Application
```bash
streamlit run app.py

# Output:
# You can now view your Streamlit app in your browser.
# Local URL: http://localhost:8501
# Network URL: http://xxx.xxx.x.x:8501
```

The application will automatically open in your default browser.

---

## 📝 Sample Queries to Test

Once the app is running, try these queries in the chat interface:

- "Show me all Python developers"
- "Find candidates with more than 3 years of experience"
- "List candidates with SQL skills"
- "Show me candidates with both Python and JavaScript skills"
- "Find senior developers with 5+ years experience"
- "Show all candidates with machine learning skills"
- "Which candidates have worked at Microsoft?"
- "Show me fresh graduates with less than 1 year experience"

---