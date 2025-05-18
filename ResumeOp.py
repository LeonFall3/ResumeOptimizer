from openai import OpenAI
from markdown import markdown
from weasyprint.text.ffi import FROM_UNITS
from weasyprint import HTML
import pdfkit

import pdfkit

# Path to the wkhtmltopdf executable
path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

def PDFcreator(html_content,response_list,type):
   if type == 'resume':
      filename = 'Resume'
   if type == 'cover':
      filename = 'CoverLetter'
   else:
      print('Invalid type selected')

   # Convert HTML to PDF
   print(f'filename Variable: {filename}')
   pdfkit.from_string(html_content, 'AlexSharp-'+filename+'.pdf', configuration=config)

   # save as markdown
   output_file = "templates/"+filename+"_new.md"

   with open(output_file, "w", encoding="utf-8") as file:
      file.write(response_list[0])



print('Select resume template: ')
print('Data, PM, Gen')
tempSelection = input().lower()
if tempSelection == 'data':
   tempSelection = 'resume'
elif tempSelection == 'pm':
   tempSelection = 'PM_resume'
else:
   tempSelection = 'Gen_resume'
   
# Open and read the Markdown file
with open(f"templates/{tempSelection}.md", "r", encoding="utf-8") as file:
   resume_string = file.read()

# input job description
print("Enter the job description:")
jd_string = input()  


RES_prompt_template = lambda resume_string, jd_string : f"""
You are a professional resume optimization expert specializing in tailoring resumes to specific job descriptions. Your goal is to optimize my resume and provide actionable suggestions for improvement to align with the target role.

### Guidelines:
1. **Relevance**:  
   - Prioritize experiences, skills, and achievements **most relevant to the job description**.  
   - Remove or de-emphasize irrelevant details to ensure a **concise** and **targeted** resume.
   - Limit work experience section to 2-3 most relevant roles and is is ordered by **most recent** to **least recent**.
   - Limit bullet points under each role to 2-3 most relevant impacts

2. **Action-Driven Results**:  
   - Use **strong action verbs** and **quantifiable results** (e.g., percentages, revenue, efficiency improvements) to highlight impact.  

3. **Keyword Optimization**:  
   - Integrate **keywords** and phrases from the job description naturally to optimize for ATS (Applicant Tracking Systems).  

4. **Additional Suggestions** *(If Gaps Exist)*:  
   - If the resume does not fully align with the job description, suggest:  
     1. **Additional technical or soft skills** that I could add to make my profile stronger.  
     2. **Certifications or courses** I could pursue to bridge the gap.  
     3. **Project ideas or experiences** that would better align with the role.  

5. **Formatting**:  
   - Output the tailored resume in **clean Markdown format**.  
   - Include an **"Additional Suggestions"** section at the end with actionable improvement recommendations.  

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

   

   # save as PDF
   output_pdf_file = "templates/"+filename+"_new.pdf"

   # Convert Markdown to HTML
   html_content = markdown(response_list[0])

   return html_content, response_list

res_html_contet, res_response_list = RunPrompt(RES_prompt, api_key, 'resume')

PDFcreator(res_html_contet,res_response_list,'resume')
print('Resume optimization completed successfully!')

with open(f"templates/resume_new.md", "r", encoding="utf-8") as file:
   resume_string = file.read()

CL_prompt_template = lambda resume_string, jd_string : f"""
You are a professional cover letter writter expert specializing in tailoring cover letters to specific job descriptions based on a given resume. Your goal is to create my cover letter and provide actionable suggestions for improvement to align with the target role.

### Guidelines:
1. Address the hiring manager professionally (use "Dear Hiring Manager" if no name is provided).
2. Express enthusiasm for the role and company, demonstrating an understanding of their mission and values.
3. Highlight relevant skills and experiences from the resume that align with the job description.
4. Showcase key accomplishments that demonstrate the candidate's ability to succeed in the role.
5. Emphasize soft skills and company culture fit (e.g., teamwork, adaptability, leadership, inclusivity).
6. Close with a strong call to action, inviting further discussion or an interview opportunity.

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

PDFcreator(cl_html_contet,cl_response_list,'cover')

print("Cover Letter creation completed successfully!")

