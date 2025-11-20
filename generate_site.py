import json
from jinja2 import Environment, FileSystemLoader
import datetime
import os

# --- Step 1: Your Information ---
# This dictionary holds all the content for your website.
WEBSITE_DATA = {
    "name": "Alex P. Günsberg",

    # FINAL CONSENSUS HEADLINE:
    "headline": "PhD Candidate, Hanken School of Economics | Visiting Scholar, UNC Kenan-Flagler",

    "image_url": "Alex_Gunsberg_web_half.jpg",

    # FINAL BIO:
    "about_me": """PhD candidate in Finance specializing in Household Finance, Behavioral Finance, 
    and Urban Economics, with a focus on consumer credit and default prediction. I apply machine 
    learning and data-driven analysis to real-world financial behaviors and policy challenges. Currently 
    visiting scholar at UNC Kenan-Flagler Business School. Interested in collaborations that bridge research 
    with practical insights, including with fintech firms, policymakers, and hedge funds.""",

    "education": {
        "phd": {
            "degree": "Ph.D. in Finance",
            "program": "Graduate School of Finance (GSF)",
            "program_url": "https://gsf.aalto.fi",
            "institution": "Hanken School of Economics",
            "period": "September 2021 – Present",
            "location": "Helsinki, Finland",
            "description": "Finland's national doctoral program in finance. Joint venture of seven "
                           "universities. Recent graduate placements include London Business School, Imperial "
                           "College London, Ohio State University, and Erasmus Rotterdam.",
            "supervisors": [
                "Professor Camelia M. Kuhnen (UNC Kenan-Flagler Business School)",
                "Professor Anders Löflund (Hanken School of Economics)"
            ]
        },
        "networks": [
            {
                "name": "Nordic Finance Network (NFN)",
                "url": "https://nfn.aalto.fi",
                "description": "Selective doctoral training network for Nordic finance researchers. Members "
                               "collaborate on empirical research and present at network workshops."
            }
        ],

        "visiting": {
            "position": "Visiting Scholar",
            "institution": "UNC Kenan-Flagler Business School",
            "period": "January 2025 – December 2026",
            "location": "Chapel Hill, North Carolina, USA",
            "host": "Professor Camelia M. Kuhnen"
        },

    },

    "links": [
        {
            "text": "CV",
            "url": "cv_alexgunsberg_public.pdf",
            "svg_path": "M21.172 5.172l-1.414 1.414-2.828-2.828 1.414-1.414q0.293-0.293 0.707-0.293t0.707 0.293l1.414 1.414q0.293 0.293 0.293 0.707t-0.293 0.707zM3 21v-15h11v3h6v12h-17zM13 9h-8v10h8v-10zM15 11.828v-0.828h2v1h-1.172l-3.328 3.328v0.828h-2v-1h1.172l3.328-3.328zM15 19v-1.172l-3.328-3.328h-0.828v-2h-1v1.172l3.328 3.328h0.828v2h1z"
        },
        {
            "text": "LinkedIn",
            "url": "https://www.linkedin.com/in/gunsberg/",
            "svg_path": "M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"
        },
        {
            "text": "SSRN",
            "url": "https://papers.ssrn.com/Sol3/Cf_Dev/AbsByAuth.cfm?per_id=1153517",
            "svg_path": "M21.57,6.37l-3.34-3.34a1.22,1.22,0,0,0-1.73,0L2.37,17.15a1.22,1.22,0,0,0,0,1.73l3.34,3.34a1.22,1.22,0,0,0,1.73,0L21.57,8.1a1.22,1.22,0,0,0,0-1.73ZM7.88,19.44,5.12,16.68l9.37-9.37,2.76,2.76Zm10.19-10.19L15.31,6.5l2.76-2.76,2.76,2.76Z"
        },
        {
            "text": "ORCID",
            "url": "https://orcid.org/0000-0002-2854-7628",
            "svg_path": "M12 0C5.372 0 0 5.373 0 12s5.372 12 12 12 12-5.373 12-12S18.628 0 12 0m0 2.667c5.133 0 9.333 4.201 9.333 9.333s-4.201 9.333-9.333 9.333S2.667 17.133 2.667 12 6.867 2.667 12 2.667m2.84 9.714c.266.001.48-.213.479-.479 0-.266-.214-.48-.48-.479-.266 0-.48.213-.479.479 0 .266.214.48.48.479m0-2.667c.71 0 1.287-.577 1.287-1.286 0-.71-.577-1.287-1.287-1.287s-1.286.577-1.286 1.287.576 1.286 1.286 1.286m2.666 4c0 1.333.444 2.667 1.333 2.667.889 0 .889-1.333 1.777-1.333s.889 1.333 1.778 1.333 1.333-1.334 1.333-2.667c0-1.334-.444-2.667-1.333-2.667-.889 0-.889 1.334-1.778 1.334s-.889-1.334-1.778-1.334c-.889 0-1.333 1.333-1.333 2.667m-5.84-1.333h-.667c-.888 0-1.333.444-1.333 1.333v2c0 .889.445 1.334 1.333 1.334h.667c.889 0 1.334-.445 1.334-1.334v-2c0-.889-.445-1.333-1.334-1.333m0 3.333h-.667c-.445 0-.667-.222-.667-.667v-2c0-.444.222-.666.667-.666h.667c.444 0 .667.222.667.666v2c0 .445-.223.667-.667.667m-2.666-3.333h-.667c-.444 0-.666.444-.666 1.333v2c0 .889.222 1.334.666 1.334h.667c.445 0 .667-.445.667-1.334v-2c0-.889-.222-1.333-.667-1.333m0 3.333h-.667c-.222 0-.333-.222-.333-.667v-2c0-.444.111-.666.333-.666h.667c.222 0 .333.222.333.666v2c0 .445-.111.667-.333.667m5.84-5.333v2.667h1.333v-2.667"
        },
        {
            "text": "Google Scholar",
            "url": "https://scholar.google.com/citations?user=JqmhniAAAAAJ&hl=en",
            "svg_path": "M12 24a7 7 0 1 1 7-7 7 7 0 0 1-7 7zm0-10a3 3 0 1 0 3 3 3 3 0 0 0-3-3zm0 8a5 5 0 1 0 5 5 5 5 0 0 0-5-5zM12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm0 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"
        },
        {
            "text": "Hanken Profile",
            "url": "https://harisportal.hanken.fi/en/persons/alex-g%C3%BCnsberg/",
            "svg_path": "M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"
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
        "Urban Economics",
        "Consumer Credit and Defaults",
    ],

    "publications": [
        {
            "title": "Misconceived Rejections: Equilibrium Effects of Fairness Constraints in Algorithmic Lending"
                     "Constraints in Algorithmic Lending",
            "is_jmp": True,
            "authors": "Alex P. Günsberg",
            "journal": "Working Paper",
            "bibtex": "",
            "abstract": "This study uses Finnish loan applicant data from 2019-2024, where financial "
                        "delinquency outcomes are observed for everyone—even those applicants rejected for "
                        "the loan—to reveal post-application outcomes. Fairness constraints—for example, U.S. "
                        "Special Purpose Credit Programs under the Equal Credit Opportunity Act or the EU AI "
                        "Act—distort markets by focusing on the intermediate phase (approval rates) rather than "
                        "optimizing the true outcome (post-loan results). Simulations show these policies ignore "
                        "asymmetric costs (one default offsets six good loans), shrinking lending by 2.1%. Causal "
                        "estimates find loan take-up raises default risk by 55.6 percentage points for marginal "
                        "borrowers. Rejections protect vulnerable applicants from intentional and non-intentional "
                        "risky borrowing behaviors. Centralized default data for algorithmic training and risk "
                        "disclosures to applicants expand access by maximizing market size.",
            "paper_url": "",
            "code_url": "",
            "slides_url": "",
            "presentations": []  # ← Placeholder for future presentations
        },
        {
            "title": "Learning How to Borrow in a Fintech World",
            "authors": (
                    "Alex P. Günsberg, "
                    "<a href=\"https://sites.google.com/view/cameliakuhnen/\" "
                    "target=\"_blank\" rel=\"noopener noreferrer\">Camelia M. Kuhnen</a>"
                ),
            "journal": "Working Paper",
            "bibtex": "",
            "abstract": "Online loan marketplaces are changing consumer lending.  Here we investigate how consumers search, learn, and make borrowing choices in this new type of market, which is characterized by close to zero search costs. We use administrative data from a large online consumer lending platform, covering 730,000 loan applications, 750,000 resulting loan offers, and more than 200,000 individuals in Finland, and supplement this with credit registry data. We document four facts. First, there are high benefits to search, as there exists significant within-applicant dispersion in terms offered by lenders. Second, soft nudges by the platform help consumers make loan choices. Third, applicants search significantly, by applying multiple times, asking for loans with different terms, and rejecting a majority of offers, in ways that suggest that individuals understand their type as borrowers. Fourth, this is a dynamic adverse selection environment, as lenders are less likely to make loans to repeat applicants, who are inferred to be worse types, which implies that consumers' search strategy need to balance informational benefits and reputational costs.",
            "paper_url": "",
            "code_url": "",
            "slides_url": "",
            "presentations": [  # ← List of presentations for THIS paper
                {
                    "venue": "HEC Lausanne and EPFL",
                    "year": 2025,
                    "presenter": "Camelia M. Kuhnen"
                },
                {
                    "venue": "University of Geneva",
                    "year": 2025,
                    "presenter": "Camelia M. Kuhnen"
                },
                {
                    "venue": "American University",
                    "year": 2025,
                    "presenter": "Camelia M. Kuhnen"
                },
                {
                    "venue": "NYU Stern",
                    "year": 2025,
                    "presenter": "Camelia M. Kuhnen"
                },
                {
                    "venue": "University of Michigan",
                    "year": 2024,
                    "presenter": "Camelia M. Kuhnen"
                },
                {
                    "venue": "FDIC",
                    "year": 2024,
                    "presenter": "Camelia M. Kuhnen"
                },
                {
                    "venue": "Erasmus University Rotterdam",
                    "year": 2024,
                    "presenter": "Camelia M. Kuhnen"
                },
                {
                    "venue": "HEC Montreal",
                    "year": 2024,
                    "presenter": "Camelia M. Kuhnen"
                },
                {
                    "venue": "Federal Reserve Bank of Philadelphia",
                    "year": 2024,
                    "presenter": "Camelia M. Kuhnen"
                },
                {
                    "venue": "University of South Carolina",
                    "year": 2024,
                    "presenter": "Camelia M. Kuhnen"
                }
            ]
        },
        {
            "title": "(Title TBD)",
            "authors":  (
                "Alex P. Günsberg, "
                "<a href=\"https://sites.google.com/view/cameliakuhnen/\" "
                "target=\"_blank\" rel=\"noopener noreferrer\">Camelia M. Kuhnen</a>, "
                "<a href=\"https://yunzhihu.web.unc.edu/\" "
                "target=\"_blank\" rel=\"noopener noreferrer\">Yunzhi Hu</a>"
            ),
            "journal": "",
            "bibtex": "",
            "abstract": "",
            "paper_url": "",
            "code_url": "",
            "slides_url": "",
            "presentations": []  # ← Placeholder for future presentations
        }
    ],

    "teaching": [
        "Thesis supervisor for 30+ M.Sc. and B.Sc. students (2021–2025)",
        "Chairman for 44 M.Sc. and B.Sc. Seminars (2021–2024)",
        "Grading over 100 referee reports and seminar presentations (2021–2024)",
        "Mentee in Hanken's Teacher Mentor Program, Pilot group (2022)"
    ],

    # In WEBSITE_DATA
    "awards_and_grants": "Secured funding from over 15 competitive grants for research, travel, and "
                         "working support from various economic, research, and cultural foundations.",

    "industry_experience": [
        {
            "role": "Entrepreneur & Co-Founder",
            "organization": "Multiple startups",
            "period": "April 2010 – August 2025",
            "description": "Over 10 years as an entrepreneur: founded multiple ventures, raised €3M+ "
                           "from VCs and angels, and sold two companies (omadesign.fi, brandphoto.fi). "
                           "Gained hands-on insights into fintech metrics like user acquisition costs, "
                           "mirroring delinquency forecasting.",
            "highlight": "Startups",
        },
        {
            "role": "Data Scientist",
            "organization": "Silicon Labs (formerly NASDAQ-listed semiconductor)",
            "period": "September 2020 – August 2021",
            "description": "Built end-to-end forecasting pipelines (MSSQL → AWS ML → Tableau) on transactional "
                           "data—analogous to ingesting lender tapes for ABS default models.",
            "highlight": "Tech/Data Science",
        },
        {
            "role": "Senior Sales Manager",
            "organization": "Estlander & Partners (algorithm-based hedge fund, cta)",
            "period": "January 2011 – February 2013",
            "description": "Managed sales for a quantitative hedge fund; gained deep exposure to systematic "
                           "trading strategies, now informing my research on consumer behavior and default prediction.",
            "highlight": "Hedge Funds",
        },
    ],

    # Technical Skills:
    "technical_skills": {
        "python_data_science": {
            "description": "Applied in quantitative finance research and analysis of large-scale datasets, "
                           "including panel data wrangling, econometric modeling, machine learning for behavioral "
                           "default predictions, and processing transaction-level credit data for risk forecasting.",
            "tools": ["Python", "Pandas/Polars", "XGBoost", "Neural Networks", "CausalML", "Survival Models",
                      "SciPy", "Statsmodels", "Linearmodels", "Scikit-learn", "Matplotlib", "Seaborn",
                      ]
        },
        "research_and_reporting": {
            "description": "Standard tools for version control, collaboration, academic publishing, and "
                           "reproducible research pipelines.",
            "tools": ["Git", "LaTeX", "IDE", "Jupyter/Colab"]
        },
        "data_engineering_and_cloud": {
            "description": "Tools for managing and processing high-volume financial datasets, including "
                           "ETL pipelines for transaction-level data and cloud-based workflows.",
            "tools": ["AWS S3/EC2", "SQLAlchemy", "SQL", "Dask", "ETL Frameworks"]
        },
    }
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
        print("Please ensure 'template.html' is in the same directory as this script.")
        print("--- End Debug ---")
        return # Exit the script
    print("--- End Debug ---\n")
    # --- END DEBUGGING ---

    # Add current year to data for footer
    WEBSITE_DATA['current_year'] = datetime.datetime.now().year

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('.')) # Looks for templates in the current directory
    template = env.get_template('template.html')

    # Render the template with your data
    html_content = template.render(WEBSITE_DATA)

    # Write the rendered HTML to index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Successfully generated index.html with updated content!")

if __name__ == '__main__':
    main()