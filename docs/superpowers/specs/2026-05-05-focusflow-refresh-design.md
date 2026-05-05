# FocusFlow Refresh Design

## Goal

Refresh the existing Django task manager so it feels more polished and intentional without changing its core information architecture or workflow. The app will be renamed to `FocusFlow` and updated with a warm, professional visual identity.

## Scope

This refresh covers lightweight branding and UI polish only:

- Rename visible product branding to `FocusFlow`
- Unify the login page and shared app layout under one visual style
- Refresh colors, spacing, typography, card treatment, and buttons
- Keep existing routes, templates, task flows, and data model intact

Out of scope:

- New features or changed user workflows
- Large template rewrites
- Database or backend behavior changes

## Visual Direction

The design direction is a warm productivity tool rather than a generic bootstrap dashboard.

- Backgrounds: soft sand, cream, and muted beige tones
- Surfaces: off-white cards with subtle borders and softer shadows
- Text: charcoal or dark navy for stronger contrast without pure black harshness
- Accent: restrained olive-gold or muted brass tones for highlights and primary actions
- Mood: focused, calm, premium, practical

## Branding

The product name will be standardized as `FocusFlow` across the app.

Branding updates include:

- Page `<title>` values
- Navbar brand text
- Login screen title and supporting copy
- High-visibility page headers where current wording feels too generic

## Layout Changes

### Shared Layout

`templates/base.html` will become the main source of the new identity.

- Replace the dark navbar with a lighter branded navigation bar
- Move visual styling from scattered inline choices toward a more coherent shared style
- Improve vertical rhythm and container spacing
- Keep current navigation structure and auth actions

### Login Screen

`templates/registration/login.html` will be brought into the same system rather than looking like a separate mini-site.

- Use the same palette and tone as the shared layout
- Improve hierarchy around the logo, heading, and form card
- Keep the form structure simple and recognizable

### Task Screens

Task list and supporting task pages will receive light-touch polish only.

- Improve header spacing and button styling
- Make cards and lists feel more consistent with the new brand
- Preserve current page organization and template logic

## Styling Strategy

The visual refresh should favor consistency over one-off overrides.

- Consolidate reusable styling in the existing app stylesheet where practical
- Keep only truly page-specific styles inline if needed
- Prefer CSS custom properties for core colors so the palette is easy to adjust
- Avoid introducing a design system heavier than the project needs

## Interaction Notes

- Existing dark mode behavior should be reviewed for visual compatibility
- If dark mode clashes with the new brand, it may be simplified rather than deeply redesigned
- Hover, focus, and button states should feel deliberate but subtle

## Testing

Verification should focus on UI stability rather than backend behavior.

- Load the login page and main task pages locally
- Confirm branding changes appear consistently
- Check layout on desktop and a narrow mobile viewport
- Ensure existing navigation and auth actions still work

## Risks

- Shared styles may unintentionally affect multiple templates at once
- Inline styles in existing templates may fight the new stylesheet if not cleaned up carefully
- Dark mode may require selective adjustment to avoid inconsistent colors

## Implementation Shape

Expected files include:

- `templates/base.html`
- `templates/registration/login.html`
- `tasks/static/tasks/css/style.css.css`
- One or more task templates for small wording or spacing adjustments

The implementation should stay incremental: establish the shared style first, then tune the login page, then spot-fix key task screens.
