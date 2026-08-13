# netlify.toml Guide

> Portable Codex-Hermes-Claude replacement authored by Rylai.

Keep configuration minimal and validate it against the installed Netlify CLI.

```toml
[build]
  command = "npm run build"
  publish = "dist"
```

SPA fallback when the application uses client-side routing:

```toml
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

Redirect:

```toml
[[redirects]]
  from = "/old"
  to = "/new"
  status = 301
```

Header:

```toml
[[headers]]
  for = "/*"

  [headers.values]
    X-Content-Type-Options = "nosniff"
```

Rules:

- Do not commit secrets to this file.
- Keep paths relative to the repository root.
- Avoid broad redirects that shadow real files or functions.
- Match the build command to the repository's lockfile and scripts.
- Test configuration with a preview deploy before production.
