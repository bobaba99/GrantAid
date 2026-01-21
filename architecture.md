# Overview

This web app will help Quebec graduate student apply to grant and fundings.

Supported list of grant and fundings:

- [CIHR](https://cihr-irsc.gc.ca/e/193.html)
- [FRQS](https://frq.gouv.qc.ca/en/health/)
- [NSERC](https://nserc-crsng.canada.ca/en)

Student would input their:

1. Personal experiences
2. Professional experiences
3. Research field - one paragraph summary
4. Research project - one paragraph summary

The web app contains the mission statements/values/objectives from above institutions and document checklists for each application.

Commonly required documents

- CV (moving towards Tri-agency CV for CIHR)
- Research statement (500 words explaining your research, someone outside your field can understand it too)
    - https://cihr-irsc.gc.ca/e/54275.html
    - https://cihr-irsc.gc.ca/e/53574.html

# User functions

1. Registration via email
2. Login via email
3. Store their inputs
4. Present application requirements and document checklist (interactive)
5. Compare differences between the requirements between the previous and current application cycle
6. LLM guidance
    1. Generate a list of recommended personal and professional experiences for CV and research statement
    2. Generate a one-paragraph summary/rationale that align student’s research with institution objectives/values/missions
7. Generate formatted CV

# Tech stack

- **Backend & Database:** Supabase (PostgreSQL + Auth + Edge Functions)
- **Service Layer:** Python (FastAPI) for complex logic & scraping
- **AI Model:** Gemini 3 (via Google AI Studio API)
- **Frontend:** React / Next.js with Tailwind CSS
- **Hosting:** Render (Web Service) + Vercel (Frontend optional)

Compile in Docker: `docker-compose up --build`

# Database Schema (Draft)

## Users & Profiles

- `profiles`: Stores user details (academic background, field of study).
    - Columns: `id` (FK to auth.users), `full_name`, `program_level` (Master's/PhD), `research_field`, `institution`.

## Experience Bank

- `experiences`: Central repository of user's history to be remixed for different applications.
    - Columns: `id`, `user_id`, `type` (Professional, Academic, Volunteer, Research), `title`, `organization`, `start_date`, `end_date`, `description`, `key_skills` (array).

## Fundings & Requirements

- `funding_definitions`: Stores static info about grants.
    - Columns: `id`, `name` (e.g., "CIHR CGS-M"), `agency` (CIHR, NSERC...), `cycle_year` (2025-2026), `deadline`, `website_url`.
- `requirements`: Specific requirements for a grant.
    - Columns: `id`, `funding_id`, `category` (CV, Statement, Transcript), `description`, `max_words`, `format_rules` (JSON).

## Applications

- `applications`: Tracks a user's progress on a specific grant.
    - Columns: `id`, `user_id`, `funding_id`, `status` (Draft, In Review, Submitted), `created_at`.
- `application_documents`: Generated content for an application.
    - Columns: `id`, `application_id`, `type` (CV, Research Statement), `content` (Markdown/Text), `version`.

# Feature Specifications

## Experience "Story-teller" (LLM)

- **Input:** User's `experiences` + specific grant's `values/mission`.
- **Process:** LLM rewrites the experience descriptions to highlight keywords relevant to the agency (e.g., highlighting "health impact" for CIHR vs. "technical innovation" for NSERC).
- **Output:** Tailored bullet points for the CV.

# Security & Privacy

- **Supabase RLS (Row Level Security):** Strict policies ensuring users can only read/write their own data.
- **Data Minimization:** LLM prompts should anonymize sensitive PII where possible, or use enterprise/private API tiers if available.

# Future Improvements

- [ ] Refined 1-10 rating criteria for funding applications
- [x] Beautify UI