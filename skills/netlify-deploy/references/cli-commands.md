# Netlify CLI Commands

> Portable Codex-Hermes-Claude replacement authored by Rylai.

Verify the installed CLI help before using a flag because commands can change.

```bash
npx netlify --help
npx netlify status
npx netlify login
npx netlify link
npx netlify init
npx netlify dev
npx netlify deploy
npx netlify deploy --prod
npx netlify open
```

Common explicit deploy inputs:

```bash
npx netlify deploy --dir dist
npx netlify deploy --build
npx netlify deploy --prod --dir dist
```

Use preview deploys before production. Read the URL and deploy status from the
actual command output. Never infer success from process startup alone.

For environment variables, prefer the Netlify dashboard or the CLI command
shown by the installed version's help. Do not print secret values.
