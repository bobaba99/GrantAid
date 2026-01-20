Generate a responsive web UI for a funding application assistant for graduate students.

Name: GrantAid

Goal:
The web app does not handle the actual application process, but instead provides a checklist-driven workflow with document uploads, deadline tracking, and AI help.

The AI assistant will evaluate the user's experiences (academic, professional, volunteer, etc.) and rate them on a scale of 1-10 based on their relevance to the funding application and agency's mission. It will also provide suggestions for how experiences should be reframed to better align with the funding application.

Style:
* Clean, academic, calm
* Light background
* Minimal visual noise

Layout:
* Left sidebar: application checklist
* Center: active form or editor
* Right panel: contextual help and AI suggestions
* Top bar: app title + user profile

Screens:

1. Dashboard
   * List of applications (only CIHR and FRQS, user cannot add more)
      * Each experience will be a card with a rating and a suggestion inside the application workspace.
      * Each experience will be a card with option to edit and delete in profiles.
   * Status: Not started / In progress / Submitted

2. Application workspace
   * Three-column layout (sidebar / main / help)
   * Checklist + form

3. Document manager
   * Upload CV (via copy and paste)
   * Describe research field - one paragraph summary
   * Research project - one paragraph summary
   * States: missing, uploaded, error

4. Deadline tracker
   * Timeline or calendar

UI components:
* Buttons, cards, badges, alerts
* Clear success and error states

Accessibility:
* Minimum font size: 16px
* Keyboard navigable

Code:
* Output semantic HTML + CSS
* Use flexbox or grid
* No decorative clutter