-- Add description column if it doesn't exist
ALTER TABLE public.funding ADD COLUMN IF NOT EXISTS description TEXT;

-- Insert FRQS Doctoral
INSERT INTO public.funding (name, agency, cycle_year, deadline, website_url, description)
VALUES (
  'Doctoral Training',
  'FRQS',
  '2025-2026',
  '2025-12-17',
  'https://frq.gouv.qc.ca/en/program/doctoral-training-master-s-degree-holders-2025-2026/',
  '## English

### Academic record and achievements (45 points)

- Transcripts
- Recognition (prizes, awards and scholarships received)
- Relevant achievements (scientific, professional, social, etc.) and experiences (related to the research project or career path)
- Capacity for commitment and leadership (in and outside of academia)
- Ability to foster dialogue between science and society

### Research project (55 points)

- Originality of the project and potential contribution to the advancement of knowledge
- Clarity and coherence of the research problem
- Relevance of the conceptual framework and methodology
- Project feasibility and timeline realism

## Entry into force of the rules

These rules apply to the 2026-2027 financial year.

## French

### Dossier académique et réalisations (45 points)

- Relevés de notes
- Reconnaissances (prix, distinctions et bourses obtenus)
- Réalisations (d’ordre scientifique, professionnel, social, etc.) et expériences pertinentes (en lien avec le projet de recherche ou le parcours)
- Capacité d’engagement et de leadership (dans et hors du milieu académique)
- Aptitudes à faire dialoguer la science et la société

### Projet de recherche (55 points)

- Originalité du projet et potentiel de contribution à l’avancement des connaissances
- Clarté et cohérence de la problématique de recherche
- Pertinence du cadre conceptuel et de la méthodologie
- Faisabilité du projet et réalisme du calendrier

## Entrée en vigueur des règles

Les présentes règles s’appliquent à l’exercice financier 2026-2027.'
);

-- Insert FRQS Master
INSERT INTO public.funding (name, agency, cycle_year, deadline, website_url, description)
VALUES (
  'Master''s Training',
  'FRQS',
  '2025-2026',
  '2025-10-01',
  'https://frq.gouv.qc.ca/en/program/masters-training-2025-2026/',
  '## English

### Academic record and achievements (50 points)

- Transcript of grades
- Recognition (prizes, awards and scholarships received)
- Relevant achievements (scientific, professional, social, etc.) and experiences (related to the proposed research or career path)

### Interest and potential in research (45 points)

- Originality, clarity and coherence of the proposed research
- Relevance of the overview of the conceptual framework and methodological elements

### General presentation of the case (5 points)

## French

### Dossier académique et réalisations (50 points)

- Relevé de notes
- Reconnaissances (prix, distinctions et bourses obtenus)
- Réalisations (d’ordre scientifique, professionnel, social, etc.) et expériences pertinentes (en lien avec la recherche proposée ou le parcours)

### Intérêt et potentiel en recherche (45 points)

- Originalité, clarté et cohérence de la recherche proposée
- Pertinence de l’aperçu du cadre conceptuel et des éléments de méthodologie

### Présentation générale du dossier (5 points)'
);

-- Insert CIHR Doctoral
INSERT INTO public.funding (name, agency, cycle_year, deadline, website_url, description)
VALUES (
  'CGS Doctoral Awards',
  'CIHR',
  '2025-2026',
  '2025-12-17',
  'https://cihr-irsc.gc.ca/e/193.html',
  '- Research potential (Weight: 50%)
    - Indicators of research potential:
        - quality of research proposal:
            - specific, focused and feasible research question(s) and/or objective(s)
            - clear description and soundness of the proposed methodology
            - significance and expected contributions to research
        - demonstration of potential to carry out proposed research relative to the stage of study, lived experience and knowledge systems
        - quality of contributions and extent to which they advance the field of research–contributions may include publications, patents, reports, posters, abstracts, monographs, presentations, creative outputs, knowledge translation outputs, community products, etc.
        - demonstration of sound judgment and ability to think critically
        - demonstration of responsible and ethical research conduct, including honest and thoughtful inquiry, rigorous analysis, commitment to safety and dissemination of research results and adherence to professional standards
        - demonstration of originality, initiative, autonomy, relevant community involvement and outreach
        - ability to communicate theoretical, technical and/or scientific concepts clearly and logically in written and oral formats
- Relevant experience and achievements obtained within and beyond academia (Weight: 50%)
    - Indicators of relevant experience and achievements obtained within and beyond academia:
        - relevant training, such as academic training, lived experience and traditional teachings
        - scholarships, awards and distinctions (amount, duration, and prestige)
        - academic record:
            - transcripts
            - duration of previous studies
            - program requirements and courses pursued
            - course load
            - relative standing (if available)
        - professional, academic, and extracurricular activities, as well as collaborations with supervisors, colleagues, peers, students and members of the community, such as:
            - teaching, mentoring, supervising and/or coaching
            - managing projects
            - participating in science and/or research promotion
            - participating in community outreach, volunteer work, and/or civic engagement
            - chairing committees and/or organizing conferences and meetings
            - participating in departmental or institutional organizations, associations, societies and/or clubs'
);

-- Insert CIHR Master
INSERT INTO public.funding (name, agency, cycle_year, deadline, website_url, description)
VALUES (
  'CGS Master''s Awards',
  'CIHR',
  '2025-2026',
  '2025-12-01',
  'https://cihr-irsc.gc.ca/e/193.html',
  '- Academic excellence (Weight: 50%): As demonstrated by past academic results, transcripts, awards and distinctions.
    - Indicators of academic excellence:
        - academic record
        - scholarships and awards held
        - duration of previous studies
        - type of program and courses pursued
        - course load
        - relative standing (if available)
- Research potential (Weight: 30%): As demonstrated by the applicant’s research history, their interest in discovery, the proposed research, its potential contribution to the advancement of knowledge in the field and any anticipated outcomes.
    - Indicators of research potential:
        - quality and originality of contributions to research and development
        - relevance of work experience and academic training to field of proposed research
        - significance, feasibility and merit of proposed research
        - sound judgment and ability to think critically
        - ability to apply skills and knowledge
        - initiative and autonomy
        - research experience and achievements relative to expectations of someone with the applicant’s academic experience
- Personal characteristics and interpersonal skills (Weight: 20%): As demonstrated by the applicant’s past professional and relevant extracurricular interactions and collaborations.
    - Indicators of personal characteristics and interpersonal skills:
        - work experience
        - leadership experience
        - project management, including organizing conferences and meetings
        - ability or potential to communicate theoretical, technical or scientific concepts clearly and logically in written and oral formats
        - involvement in academic life
        - volunteerism/community outreach
');