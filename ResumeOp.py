# from IPython.display import display, Markdown
from openai import OpenAI

from markdown import markdown
from weasyprint.text.ffi import FROM_UNITS
from weasyprint import HTML

# Open and read the Markdown file
with open("templates/resume.md", "r", encoding="utf-8") as file:
    resume_string = file.read()

# input job description
print("Enter the job description:")
jd_string = input()  


prompt_template = lambda resume_string, jd_string : f"""
You are a professional resume optimization expert specializing in tailoring resumes to specific job descriptions. Your goal is to optimize my resume and provide actionable suggestions for improvement to align with the target role.

### Guidelines:
1. **Relevance**:  
   - Prioritize experiences, skills, and achievements **most relevant to the job description**.  
   - Remove or de-emphasize irrelevant details to ensure a **concise** and **targeted** resume.
   - Limit work experience section to 2-3 most relevant roles
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

prompt = prompt_template(resume_string, jd_string)

# Import the necessary module
from dotenv import load_dotenv
import os

# Load environment variables from the .env file (if present)
load_dotenv()

# Access environment variables as if they came from the actual environment
api_key = os.getenv('OPENAI_API_KEY')

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
response_list = response_string.split("## Additional Suggestions")

import pdfkit

# Path to the wkhtmltopdf executable
path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

# save as PDF
output_pdf_file = "templates/resume_new.pdf"

# Convert Markdown to HTML
html_content = markdown(response_list[0])


# Convert HTML to PDF
pdfkit.from_string(html_content, 'output.pdf', configuration=config)

# save as markdown
output_file = "templates/resume_new.md"

with open(output_file, "w", encoding="utf-8") as file:
    file.write(response_list[0])

print("Resume optimization completed successfully!")

