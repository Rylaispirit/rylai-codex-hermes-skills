# Netlify Deployment Patterns

> Portable Codex-Hermes replacement authored by Rylai.

## Static Site

- Build command: none or the project's documented build.
- Publish directory: project root or generated static directory.
- Verify `index.html` exists in the publish directory.

## Vite Or Similar SPA

- Install dependencies with the repository's package manager.
- Run the existing build script.
- Publish the generated directory, commonly `dist`.
- Add an SPA redirect only when client-side routing requires it.

## Framework Integration

Use the framework adapter already present in the repository. Do not guess the
publish directory from the framework name alone; inspect package scripts,
Netlify configuration, and build output.

## Preview Then Production

1. Run local tests and build.
2. Create a preview deploy.
3. Open the preview URL and test critical routes.
4. Confirm environment variables and serverless functions.
5. Deploy to production only with explicit approval.
6. Verify the production URL and record rollback information.

## Existing Site

Link to the intended site before deploying. Confirm the site identifier and
team. A repository name is not proof that the correct Netlify site is linked.

## Failure Triage

- Build failure: reproduce locally and inspect the first root-cause error.
- Missing publish directory: verify the build command and actual output path.
- Route 404: inspect redirects and SPA routing.
- Runtime error: inspect function or edge logs without exposing secrets.
- Wrong site: stop, verify linkage, and do not overwrite another project.
