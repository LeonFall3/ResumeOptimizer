# Resume Optimizer
Based on Shaw Talebi's AI [Builders Bootcamp Project](https://github.com/ShawhinT/AI-Builders-Bootcamp-2/tree/main/lightning-lesson)

This is a small personal project created to help my current job hunt. What better way to apply to data science and related jobs than with a project that uses the same skill set!

Updated to be more user friendly!

## How to use
1. Create a virtual environment.
2. Create an `.env` file and add `OPENAI_API_KEY=` then your own API key.
    - You will need to sign in or make an [OpenAI account](https://auth.openai.com/log-in)
    - Here is [a guide](https://addepto.com/blog/what-is-an-openai-api-and-how-to-use-it/#:~:text=Once%20you%27ve%20created%20your,%27View%20API%20keys%27%20option.) on how to do this from .addepto (may be out of date)
3. Run `SetUp.py`. This will set up your user info aswell as make sure you have all the python modules you need.
4. Put your resume(s) and cover letter templates in the `templates\` folder.
    - The cover letter template needs to be named `CL.md`.
    - Resume template names need to match the type of job name they are for. For example, if you entered "data" as a job type, the resume template for that job type needs to be named `data_resume.md`.
    - For a "general" resume template, aka not geared towards any job type, OR you are only applying for one job type, name the resume template `resume.md`.
    
<span style="color:red">*IMPORTANT*</span> Make sure you use the correct naming convention!</span>

5. Run the code and paste the job description when asked. Paste it on one line.
6. Check the `output\` folder for your optimized resume and cover letter!

<span style="color:red">*IMPORTANT*</span> Always review your output! LLMs are helpful, but can make things up. You don't want to accidently lie on your resume or cover letter!



## Trouble Shooting
You may need to download and install [wkhtmltopdf](wkhtmltopdf). If you do, please make sure to put it in `C:\Program Files\`