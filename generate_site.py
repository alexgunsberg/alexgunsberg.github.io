import json
from jinja2 import Environment, FileSystemLoader
import datetime
import os # Import the os module for debugging

# --- Step 1: Your Information ---
# This dictionary holds all the content for your website.
WEBSITE_DATA = {
    "name": "Alex Günsberg (Guensberg)",
    "headline": "PhD Candidate in Finance | Visiting Scholar at UNC Kenan-Flagler",
    "image_url": "Alex_Gunsberg_web_half.jpg",
    "about_me": "I am a PhD Candidate in Finance at the Graduate School of Finance (GSF), affiliated with the Hanken School of Economics, and a visiting scholar at the UNC Kenan-Flagler Business School. My research interests lie at the intersection of Household Finance, Behavioral Finance, and Urban Economics. In my work, I heavily utilize machine learning and Python-based data engineering skills, drawing on over a decade of industry experience. This includes exposure to systematic strategies as a Senior Sales Manager at a CTA hedge fund and honing my quantitative skills as a Data Scientist and entrepreneur. This background provides me with a unique, practice-oriented perspective on financial markets and data-driven research.",
    "links": [
        {
            "text": "LinkedIn",
            "url": "https://www.linkedin.com/in/gunsberg/",
            "svg_path": "M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"
        },
        {
            "text": "Github",
            "url": "https://github.com/alexgunsberg",
            "svg_path": "M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"
        },
        {
            "text": "DataCamp",
            "url": "https://datacamp.com/profile/alexgunsberg",
            "svg_path": "M3.5 18.5v-13l17 6.5-17 6.5zm1.5-11.338v8.676l11.056-4.338-11.056-4.338z"
        }
    ],
    "research_interests": [
        "Household Finance",
        "Behavioral Finance",
        "Urban Economics"
    ],
    "publications": [
        {
            "title": "(Job Market Paper) Misconceived Rejections: Equilibrium Effects of Fairness Constraints in Algorithmic Lending",
            "authors": "Alex Günsberg",
            "journal": "", # This line is now hidden
            "url": "#"
        },
        {
            "title": "Learning How to Borrow in a Fintech World",
            "authors": "with Camelia M. Kuhnen",
            "journal": "Working Paper. Presented at: Federal Reserve Bank of Philadelphia, University of South Carolina, HEC Montreal, Erasmus Rotterdam, FDIC, and University of Michigan (2024).",
            "url": "#"
        },
        {
            "title": "(Title TBD)",
            "authors": "with Camelia M. Kuhnen and Yunzhi Hu",
            "journal": "", # This line is now hidden
            "url": "#"
        }
    ],
    "teaching": [
        "Thesis supervisor for 30+ M.Sc. and B.Sc. students (2021-2024)",
        "Chairman for 42 B.Sc. Seminars",
        "Grading +100 referee reports and seminar presentations",
        "Mentee in Hanken’s Teacher Mentor Program, Pilot group (2022)"
    ],
    "industry_experience": [
        { "role": "Senior Sales Manager", "organization": "Estlander & Partners (CTA Hedge Fund)" },
        { "role": "Data Scientist", "organization": "Silicon Labs (formerly Nasdaq listed)" },
        { "role": "Co-Founder & Board Member", "organization": "Multiple Startups, 2012-2023" }
    ]
}

# --- Step 2: Site Generation ---
def main():
    """Main function to generate the website."""

    # --- DEBUGGING LINES ---
    print("--- Starting Debug ---")
    current_directory = os.getcwd()
    print(f"Current Working Directory: {current_directory}")
    print("Files found in this directory:")
    for filename in os.listdir('.'):
        print(f" - {filename}")

    template_path = os.path.join(current_directory, 'template.html')
    if os.path.exists(template_path):
        print("\nSUCCESS: Python's os.path.exists() CAN find template.html.")
    else:
        print("\nERROR: Python's os.path.exists() CANNOT find template.html.")
        print("--- End Debug ---")
        return # Exit the script
    print("--- End Debug ---\n")
    # --- END DEBUGGING ---


    WEBSITE_DATA['current_year'] = datetime.datetime.now().year
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')
    html_content = template.render(WEBSITE_DATA)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Successfully generated index.html with updated content!")

if __name__ == '__main__':
    main()
