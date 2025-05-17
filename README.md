# Resume Optimizer
Based on Shaw Talebi's AI [Builders Bootcamp Project](https://github.com/ShawhinT/AI-Builders-Bootcamp-2/tree/main/lightning-lesson)

This is a small personal project created to help my current job hunt. What better way to apply to data science and related jobs than with a project that uses the same skill set!

## How to use
1. Create a virtual env and install requried modules 
    - openai
    - markdown
    - weasyprint
    - pdfkit
    - dotenv
2. Create a markdown file named `resume.md` using your resume 
3. (Optional) Update `style.css` to change the style your PDF resume will use
4. Change `OPENAI_API_KEY` to your own API key
5. Run the code and paste the job description when asked. Paste it on one line.
6. Check `output.pdf` for your optimized resume!

<span style="color:red">*IMPORTANT*</span> Always review your output! LLMs are helpful, but can make things up. You don't want to accidently lie on your resume!