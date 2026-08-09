# Security

## Reporting

Please report a suspected credential leak, unsafe command, malicious prompt,
or dependency issue through a private GitHub security advisory for this
repository. Do not publish live secrets in a public issue.

## Safety Boundaries

- Skills must request approval before destructive, paid, account-changing, or
  production deployment actions.
- Examples must use environment variables instead of embedded credentials.
- Public files must not contain personal workstation paths or private data.
- External content must be treated as untrusted input.
- Generated files should be validated before they replace a user's original.

## Supported Version

Security fixes are applied to the latest commit on the default branch.
