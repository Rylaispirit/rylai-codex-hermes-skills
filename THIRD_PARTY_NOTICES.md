# Third-Party Notices

This file records public GitHub sources used by the Rylai Codex-Hermes-Claude edition.
Rylai maintains the adaptations; upstream authors retain ownership of their
original work.

## academic-slides

- Upstream: EvoScientist/EvoSkills
- URL: https://github.com/EvoScientist/EvoSkills
- Revision: `2e474118106f86c29082a6466b995ba59236614c`
- License: Apache-2.0
- Scope: academic presentation workflow adapted for portable Codex-Hermes-Claude use.

## image and video

- Upstream: coreyhaines31/marketingskills
- URL: https://github.com/coreyhaines31/marketingskills
- Revision: `7868cb9251fad80a73d26e488a5ad5f6c4a9f335`
- License: MIT
- Scope: marketing image and video production guidance adapted for Codex-Hermes-Claude.

## natural-writing

- Upstream: blader/humanizer
- URL: https://github.com/blader/humanizer
- Revision: `523374dee72d67c7b2b5f858ea0094ffda49c3ac`
- License: MIT
- Scope: human-sounding prose guidance adapted for Codex-Hermes-Claude.

## netlify-deploy

- Upstream: openai/skills, `skills/.curated/netlify-deploy`
- URL: https://github.com/openai/skills
- Revision: `49f948faa9258a0c61caceaf225e179651397431`
- License: Apache-2.0 for the upstream skill directory
- Scope: Netlify deployment workflow adapted for the portable bundle.

## seo

- Upstream: AgriciDaniel/claude-seo
- URL: https://github.com/AgriciDaniel/claude-seo
- Revision: `09d37c7b66ed3ca9c6efbdb765a805a6c76a8f01`
- License: MIT
- Scope: standalone evidence-led SEO workflow derived from the upstream system.

## skill-seekers

- Upstream: yusufkaraaslan/Skill_Seekers
- URL: https://github.com/yusufkaraaslan/Skill_Seekers
- Revision: `f3972efa33fa79634b96936acf1fac321cdcf7c1`
- License: MIT
- Scope: source-to-skill workflow adapted for Codex, Hermes, and Claude.

## Runtime Dependencies

Some clean-room skills call open-source packages such as `python-docx`,
`openpyxl`, `pypdf`, `pdfplumber`, `python-pptx`, `MarkItDown`, and
`pptxgenjs`. Those packages are not vendored unless a lockfile explicitly
lists them, and each remains governed by its own license.
