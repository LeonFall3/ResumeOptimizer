import os
import json

def ensure_file_exists(filepath):
    if not os.path.exists(filepath):
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        # Create an empty file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("")

# Before opening resume_new.md
resume_md_path = f"generated//resume_new.md"
ensure_file_exists(resume_md_path)
with open(resume_md_path, "r", encoding="utf-8") as file:
    resume_string = file.read()

# Before opening coverletter_new.md
coverletter_md_path = f"generated//coverletter_new.md"
ensure_file_exists(coverletter_md_path)
with open(coverletter_md_path, "r", encoding="utf-8") as file:
    resume_string = file.read()


with open("user_info.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Check if user information is already set up
if 'user' in data:
    print("User info is already set up, are you sure you want to overwrite it? (yes/no)")
    overwrite = input().strip().lower() == 'yes'

if not overwrite:
    print("Exiting setup. You can run ResumeOp.py to generate your resume with the existing user info.")
    exit()

user_info_file = "user_info.json"

first_name = input("Enter your first name: ").capitalize()
last_name = input("Enter your last name: ").capitalize()

user = first_name+last_name

print("Are you applying for multiple types of jobs? (yes/no)")
multiple_jobs = input().strip().lower() == 'yes'

if multiple_jobs:
    print("Enter the job types you are applying for, separated by commas:")
    job_types = [jobtype.strip() for jobtype in input().split(',')]
    print("Please ensure you have a resume template for each job type in the templates folder and that the resume template's name uses the following convention:")
    print("jobtype_resume")
    print("For example, if you are applying for data science and product management jobs, you should have templates named 'data_resume.md' and 'pm_resume.md'.")
    print("Do you want to include a general resume template as well? (yes/no)")
    include_general = input().strip().lower() == 'yes'
    if include_general:
        job_types.append('resume')
        print("The general resume template needs to be named 'resume.md'.")
    else:
        print("You will not be using a general resume template.")

else:
    job_types = ['resume']
    print("You will be applying for a single type of job. The resume template will be named 'resume.md'.")

#save user info to user_info.json

user_info = {
    "user": user,
    "multiple_jobs": multiple_jobs,
    "job_types": job_types
}

with open(user_info_file, "w", encoding="utf-8") as f:
    json.dump(user_info, f)

print(f"User information saved to {user_info_file}.")
print("Setup complete. You can now run the ResumeOp.py script to generate your resume.")