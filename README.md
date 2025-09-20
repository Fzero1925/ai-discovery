# AI Discovery Static Site

AI Discovery publishes English-language AI news briefings, tool rundowns, and robotics coverage. The production repository only contains the Hugo static site; automation scripts live outside the repo. Updates happen by pushing Markdown, letting Hugo rebuild pages automatically.

- **Navigation**: News, Tools, Robot, About.
- **Content focus**: concise news context, workflow-based tool guides, and robotics updates.
- **Monetisation**: Google AdSense plus carefully selected affiliate programs.

## Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/ai-discovery.git
cd ai-discovery

# Optional - install Node dependencies if you customise styles
npm install

# Preview locally
hugo server -D
```

Automation pipelines and data assets now live beside the repo (for example `../ai-discovery-automation/`). Run scripts there, then copy finished Markdown into `content/articles/`.

## Content Workflow (Zero Maintenance)

1. Prepare a Markdown file with front matter:
   ```yaml
   ---
   title: "Sample Title"
   description: "150 characters or fewer"
   date: 2025-09-20
   categories: ["news"]
   tags: ["ai", "robotics"]
   featured_image: "/images/sample.jpg"
   image_alt: "Descriptive caption"
   draft: false
   ---
   ```
2. Save the file in `content/articles/` and assign categories that control navigation (for example `news`, `robotics`, `content-creation`).
3. Commit and push; Vercel rebuilds the static site.

## Directory Structure

```
ai-discovery/
|-- content/            # Markdown articles and static pages
|-- layouts/            # Hugo templates (homepage, sections, partials)
|-- static/             # CSS, JS, and image assets
|-- config/             # Additional configuration files
|-- dev-docs/           # Internal planning notes (gitignored when needed)
|-- config.toml         # Primary Hugo configuration
|-- README.md           # This document
`-- vercel.json         # Deployment configuration
```

## Robot Section

- `/robot/` collects industrial, service, and research robotics coverage with anchor links for quick navigation.
- Upload new robotics-related Markdown files to `content/articles/` with `categories: ["robotics"]` to surface them automatically.

## SEO and Compliance

- Templates include structured data, breadcrumbs, sitemaps, and lazy-loading helpers.
- Always use licensed imagery with meaningful `image_alt` text.
- Maintain About, Contact, Privacy, and Terms pages for AdSense compliance.

## Common Commands

```bash
hugo server -D    # Local preview
hugo --minify     # Production build (outputs to public/)
```

For internal plans and backlog items, review the Markdown files under `dev-docs/`.
