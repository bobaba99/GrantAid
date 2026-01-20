Generate a responsive web UI for an academic funding application assistant designed for graduate students.

The product simplifies funding applications by turning complex requirements into a guided, checklist-driven workflow with document management, deadline tracking, and AI assistance.

Target users:

* Graduate students (Master’s, PhD)
* Time-constrained, cognitively overloaded
* Low tolerance for bureaucratic language

Design intent:

* Visual tone: {calm | academic | professional}
* Emotional tone: {supportive | neutral}
* Trust level: {high}
* Complexity: {minimal | moderate}
* Style reference: modern academic SaaS, similar to Notion + Linear + government portals but less sterile

Layout:

* Desktop-first, fully responsive
* Grid: {12px | 16px}
* Max width: {1140px | 1280px}
* Navigation: left sidebar + top bar
* Sidebar: application list + progress indicators
* Top bar: user profile, notifications, global search

Colour:

* Primary: {#2F5D9F}
* Secondary: {#3A7F7B}
* Accent: {#F2A541}
* Background: {#F8FAFC}
* Surface: {#FFFFFF}
* Border: {#E2E8F0}
* Text primary: {#1F2933}
* Text secondary: {#4B5563}
* Success: {#2E7D32}
* Error: {#C62828}
* Accessibility target: {WCAG AA}

Typography:

* Font: {Inter | SF Pro | Source Sans}
* Headings: 600–700
* Body: 400–500
* Line height: 1.5
* Base font size: {16px}

Core screens to generate:

1. Landing page

* Headline: “Turn funding applications into a guided checklist”
* Primary CTA: “Start application”
* Secondary CTA: “Browse funding opportunities”
* Visual: dashboard preview mockup

2. Dashboard

* Application cards or table
* Status: Not started / In progress / Submitted / Awarded
* Progress: percentage bar + step counter
* Deadline warning badges

3. Application workspace (main screen)
   Three-column layout:

* Left: checklist steps

  * Eligibility
  * Required documents
  * References
  * Submission
* Center: active form/editor panel
* Right: contextual help panel

  * Plain-language explanations
  * Examples
  * AI hints

4. Document manager

* Upload CV, transcripts, proposals, letters
* States: missing, uploaded, error, validated
* Drag-and-drop upload UI

5. Deadline tracker

* Timeline view + calendar view
* Visual urgency encoding near deadlines

6. AI assistance panel

* Rewrite and polish text
* Summarize requirements
* Check compliance
* Must be visually marked as “assistive, not authoritative”

Component requirements:

* Buttons, cards, progress bars, checklists, badges, alerts
* States: default, hover, loading, success, error, disabled
* Icon style: {outline}

Interaction principles:

* Every task must feel finite and checkable
* Reduce jargon; rewrite bureaucratic language into student-friendly language
* Strong visual progress feedback
* Errors must be specific and actionable

Accessibility:

* Keyboard navigable
* Colour-blind safe
* Minimum text size: {16px}
* Clear focus states

Code output requirements:

* Generate semantic HTML + CSS
* Clean component structure
* Avoid absolute positioning unless necessary
* Responsive layout using flexbox or grid
* Layout must be implementation-ready