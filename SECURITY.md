# Security Policy

## Reporting a Vulnerability

Please report security vulnerabilities by opening an issue or contacting the maintainers directly.

## Supported Versions

We provide security updates for the latest stable version of this project.

## Scanning for Secrets

This repository uses gitleaks to scan for secrets. If you encounter false positives, please add them to the `.gitleaks.toml` allowlist.

## Dependency Security

We recommend using tools like Dependabot or Renovate to keep dependencies up-to-date.

## Secrets Management

Never commit secrets to this repository. The following patterns are automatically excluded:
- Environment files (.env, .env.local, etc.)
- Key files (*.key, *.pem, *.p12)
- Secret directories (secrets/, config/secrets.yml)

## Best Practices

- Use environment variables for all sensitive data
- Implement input validation for all user inputs
- Use parameterized queries to prevent SQL injection
- Implement rate limiting on APIs
- Add proper CORS configuration
- Implement proper authentication/authorization