from openai import OpenAI
from markdown import markdown
from weasyprint.text.ffi import FROM_UNITS

import pdfkit
import json
import os

user_info_path = "user_info.json"
# Path to the wkhtmltopdf executable
path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

import sys

if len(sys.argv) >= 3:
   job_type = sys.argv[1]
   job_description = sys.argv[2]
else:
   job_type = input("Enter job type: ")
   job_description = input("Enter job description: ")

filename = 'generated//resume_new.md'
mode = 'r'
options = {'encoding': 'UTF-8' }

if not os.path.exists(user_info_path):
   print("Please run SetUp.py first to set up your user information.")
   exit()
with open("user_info.json", "r", encoding="utf-8") as f:
   data = json.load(f)


user = data['user']
multiple_jobs = data['multiple_jobs']
job_types = data['job_types']
cover_letter = data['cover_letter']






def PDFcreator(html_content,response_list,type):
   if type == 'cover':
      filename = 'coverletter'
   else:
      filename = 'resume'


   print(f"type: {type}")
   # Convert HTML to PDF
   options = {'encoding': 'UTF-8' }
   pdfkit.from_string(html_content, f'output//{user}-{filename}.pdf', configuration=config, options=options)

   print(f"PDF created successfully: {filename}.pdf")
   print(f"md output {filename}.md")

   output_file = f"generated//{filename}_new.md"
   with open(output_file, "w", encoding="utf-8") as file:
      file.write(response_list[0])


   # Import the necessary module
from dotenv import load_dotenv
import os

   # Load environment variables from the .env file (if present)
load_dotenv()

   # Access environment variables as if they came from the actual environment
api_key = os.getenv('OPENAI_API_KEY')
from datetime import date
date = date.today()

def RunPrompt(prompt, api_key, type):
   print(f"Running prompt for {type}")
   if type == 'resume':
      filename = 'Resume'
   if type == 'cover':
      filename = 'CoverLetter'
   # setup api client
   client = OpenAI(api_key=api_key)

   # make api call
   response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
         {"role": "system", "content": "Expert resume writer"},
         {"role": "user", "content": prompt}
      ], 
      temperature = 0.7
   )

   # extract response
   response_string = response.choices[0].message.content

   # separate new resume from improvement suggestions
   response_list = response_string.split("Additional Suggestions")

   # Convert Markdown to HTML
   html_content = markdown(response_list[0])

   return html_content, response_list

# if multiple_jobs:
#    print('Select resume template')
#    print(f"Available templates: {job_types}")
#    tempSelection = job_type.lower()
#    for job_type in job_types:
#       if tempSelection == "gen" or tempSelection == "general":
#          tempSelection = "resume"
#          break
#       if tempSelection == job_type:
#          tempSelection = f"{job_type}_resume"
#          break

# else:
#    tempSelection = "resume"

# Open and read the Markdown file
with open(f"{data["resume_paths"][job_type]}", "r", encoding="utf-8") as file:
   resume_string = file.read()
# print("Enter the job description:")
jd_string = job_description


# Resume optimization
print('Resume optimization starting')
RES_prompt_template = lambda resume_string, jd_string : f"""
You are a professional resume optimization expert specializing in tailoring resumes to specific job descriptions. Your goal is to optimize my resume and provide actionable suggestions for improvement to align with the target role.

### Guidelines:
1. **Relevance**:  
   - Prioritize experiences, skills, and achievements **most relevant to the job description**.  
   - Remove or de-emphasize irrelevant details to ensure a **concise** and **targeted** resume.
   - Limit work experience section to the 3 most recent roles, listed in reverse chronological order (newest to oldest, as in the resume).
   - If the resume is longer than one page, remove less relevant experiences or details.
   - Limit bullet points under each role to 2-3 most relevant impacts

2. **Action-Driven Results**:  
   - Use **strong action verbs** and **quantifiable results** (e.g., percentages, revenue, efficiency improvements) to highlight impact.  

3. **Keyword Optimization**:  
   - Integrate **keywords** and phrases from the job description naturally to optimize for ATS (Applicant Tracking Systems) but are also related to past job experience.  

4. **Additional Suggestions** *(If Gaps Exist)*:  
   - If the resume does not fully align with the job description, suggest:  
     1. **Additional technical or soft skills** that I could add to make my profile stronger.  
     2. **Certifications or courses** I could pursue to bridge the gap.  
     3. **Project ideas or experiences** that would better align with the role.  

5. **Formatting**:  
   - Output the tailored resume in **clean Markdown format**.  
   - Include an **"Additional Suggestions"** section at the end with actionable improvement recommendations.
   - If you see the text [DATE] in the resume, replace it with today's date in the format of "Month Day, Year" (e.g., "October 1, 2023").

---

### Input:
- **My resume**:  
{resume_string}

- **The job description**:  
{jd_string}

---

### Output:  
1. **Tailored Resume**:  
   - A resume in **Markdown format** that emphasizes relevant experience, skills, and achievements.  
   - Incorporates job description **keywords** to optimize for ATS.  
   - Uses strong language and is no longer than **one page**.

2. **Additional Suggestions** *(if applicable)*:  
   - List **skills** that could strengthen alignment with the role.  
   - Recommend **certifications or courses** to pursue.  
   - Suggest **specific projects or experiences** to develop.
"""
RES_prompt = RES_prompt_template(resume_string, jd_string)
res_html_contet, res_response_list = RunPrompt(RES_prompt, api_key, 'resume')
print("Resume prompt ran")
with open(f"generated//resume_new.md", "r", encoding="utf-8") as file:
   resume_string = file.read()
# print(f"resume string: {resume_string}")
PDFcreator(res_html_contet,res_response_list,'resume')
print('Resume optimization completed successfully!')

if cover_letter:
   # Cover letter generation
   print('Cover Letter optimization starting')
   CL_prompt_template = lambda resume_string, jd_string : f"""
   You are a professional cover letter writter expert specializing in tailoring cover letters to specific job descriptions based on a given resume. Your goal is to create my cover letter and provide actionable suggestions for improvement to align with the target role.

   ### Guidelines:
   1. Address the hiring manager professionally (use "Dear Hiring Manager" if no name is provided).
   2. Express enthusiasm for the role and company, demonstrating an understanding of their mission and values.
   3. Highlight relevant skills and experiences from the resume that align with the job description.
   4. Showcase key accomplishments that demonstrate the candidate's ability to succeed in the role.
   5. Emphasize soft skills and company culture fit (e.g., teamwork, adaptability, leadership, inclusivity).
   6. Close with a strong call to action, inviting further discussion or an interview opportunity.
   7. Ensure the letter only uses acturate from the resume and job description.

   Ensure the tone is professional yet engaging, and keep the letter concise (ideally within 300-400 words). Format the response as a formal cover letter.

   ---

   ### Input:
   - **My resume**:  
   {resume_string}

   - **The job description**:  
   {jd_string}

   - **Today's Date**:
   {date}

   ---

   ### Output:  
   1. **Tailored Cover Letter**:  
      - A resume in **Markdown format** that emphasizes relevant experience, skills, and achievements.  
      - Uses strong language and is no longer than **one page**.
      - Address the hiring manager professionally
      - Express enthusiasm for the role and company
      - Highlight relevant skills and experiences from the resume
      - Showcase key accomplishments
      - Emphasize soft skills and company culture fit
      - do not use horizontal lines
      - do not write "cover letter" at the top
      - use the name formatting for the name and contact info as the resume

   2. **Additional Suggestions** *(if applicable)*:  
      - List **skills** that could strengthen alignment with the role.  
      - Recommend **certifications or courses** to pursue.  
      - Suggest **specific projects or experiences** to develop.
   """
   CL_prompt = CL_prompt_template(resume_string, jd_string)
   cl_html_contet, cl_response_list = RunPrompt(CL_prompt, api_key, 'cover')
   print("Cover Letter prompt ran")
   with open(f"generated//coverletter_new.md", "r", encoding="utf-8") as file:
      resume_string = file.read()
   # print(f"Cover Letter string: {resume_string}")
   PDFcreator(cl_html_contet,cl_response_list,'cover')
   print("Cover Letter creation completed successfully!")

