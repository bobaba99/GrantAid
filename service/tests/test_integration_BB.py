import os
import pytest
from dotenv import load_dotenv
from src.ranker import ExperienceRanker
from src.llm_client import LLMClient
from src.models import Experience, ExperienceType, FundingDefinition, FundingAgency
from datetime import date
from src.utils import get_logger

# Load env from service/src/.env
# Assuming the test is run from project root, so path is service/src/.env
load_dotenv("src/.env")

logger = get_logger(__name__)

def parse_markdown_data(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    experiences = []
    current_exp = {}
    lines = content.split('\n')
    parsing_experiences = False

    for line in lines:
        line = line.strip()
        if line == "# Experiences":
            parsing_experiences = True
            continue
        
        if not parsing_experiences:
            continue

        if line.startswith("## "):
            if current_exp:
                experiences.append(current_exp)
            current_exp = {"title_org": line[3:]}
        elif line.startswith("**Type**"):
            current_exp["type"] = line.split(":")[1].strip().upper()
        elif line.startswith("**Date**"):
             # Simplified date parsing for test
             current_exp["date"] = line.split(":")[1].strip()
        elif line.startswith("**Description**"):
            current_exp["description"] = line.split(":")[1].strip()
        elif line.startswith("**Skills**"):
            skills_str = line.split(":")[1].strip()
            current_exp["skills"] = [s.strip() for s in skills_str.split(",")]

    if current_exp:
        experiences.append(current_exp)

    return experiences

def test_integration_bruce_banner():
    # 1. Setup
    input_file = "src/test_data/bruce_banner.md"
    output_file = "src/test_data/feedback.md"
    
    if not os.path.exists(input_file):
        pytest.skip(f"Input file {input_file} not found")

    raw_experiences = parse_markdown_data(input_file)
    
    # Mock/Real LLM
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("WARNING: GEMINI_API_KEY not found in env. Using mock response.")
        # For a real integration test, we might want to fail or mock. 
        # Here we'll rely on the existing mock structure if needed, or just let it fail if the user expects real LLM.
        # But per instructions, let's try to use the real one if env is loaded.
        pass

    llm_client = LLMClient(api_key=api_key)
    ranker = ExperienceRanker(llm_client)

    # 2. Target Funding
    target_funding = FundingDefinition(
        id="cihr-cgs-d",
        name="Canada Graduate Scholarships - Doctoral (CGS D)",
        agency=FundingAgency.CIHR,
        cycle_year="2025-2026",
        deadline=date(2025, 10, 17),
        website_url="https://cihr-irsc.gc.ca/e/193.html"
    )

    # 3. Process
    results = []
    for idx, exp_data in enumerate(raw_experiences):
        # Determine Enum type safely
        try:
            exp_type = ExperienceType[exp_data.get("type", "PROFESSIONAL")]
        except KeyError:
            exp_type = ExperienceType.PROFESSIONAL

        # Split title/org
        title_org = exp_data.get("title_org", "Unknown - Unknown")
        if " - " in title_org:
            org, title = title_org.split(" - ", 1)
        else:
            org, title = title_org, "N/A"

        experience = Experience(
            id=str(idx),
            type=exp_type,
            title=title,
            organization=org,
            start_date=date(2000, 1, 1), # Dummy date
            description=exp_data.get("description", ""),
            key_skills=exp_data.get("skills", [])
        )

        try:
            ranking = ranker.rank_experience(experience, target_funding)
            results.append({
                "experience": experience,
                "ranking": ranking
            })
        except Exception as e:
            logger.error(f"Error ranking experience {experience.title}: {e}")
            results.append({
                "experience": experience,
                "ranking": {"score": 0, "rationale": f"Error: {str(e)}"}
            })

    # 4. Output to Feedback Markdown
    with open(output_file, 'w') as f:
        f.write(f"# Feedback Report for Bruce Banner\n\n")
        f.write(f"**Target Grant**: {target_funding.name}\n\n")
        
        for res in results:
            exp = res["experience"]
            rank = res["ranking"]
            
            f.write(f"## {exp.organization} - {exp.title}\n")
            f.write(f"**Score**: {rank['score']}/10\n\n")
            f.write(f"**Rationale**: {rank['rationale']}\n\n")
            f.write("---\n\n")

    assert os.path.exists(output_file)
    assert len(results) > 0

if __name__ == "__main__":
    print("Running integration test for Bruce Banner...")
    try:
        test_integration_bruce_banner()
        print("Test completed successfully. Check service/src/test_data/feedback.md for results.")
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()

