# Security Policy

## Supported Versions

This project is a collection of cybersecurity reference handbooks. As such, it is maintained as a living document with no versioned releases. Security updates are applied continuously to the main branch.

## Reporting a Vulnerability

This repository contains educational cybersecurity reference materials. If you discover a security issue or sensitive data exposure in the repository itself:

1. **Do not** open a public GitHub issue.
2. Email the maintainer directly or open a [private security advisory](https://github.com/juninmd/Awesome-Cybersecurity-Handbooks/security/advisories/new).
3. You should receive a response within 48 hours.
4. If the issue is confirmed, a fix will be prioritized and deployed.

We ask that you do not publicly disclose the issue until it has been addressed.

## Security Practices

### Secret Scanning
- [Gitleaks](https://github.com/gitleaks/gitleaks) is run on every push to detect hardcoded secrets, API keys, and credentials.
- Allowlisted false positives are maintained in `.gitleaks.toml`.
- Any real secrets found will be revoked immediately and the commit history scrubbed.

### Dependency Management
- [Dependabot](https://docs.github.com/en/code-security/dependabot) is configured for automated dependency updates.
- Dependencies are scanned weekly for known vulnerabilities.

### CI/CD Security
- CI workflows use the minimum required permissions (`contents: read`).
- Secrets are stored exclusively in [GitHub Secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions).
- No secrets or credentials are committed to the repository.

### Code of Conduct
This project follows OWASP best practices. All contributions are reviewed for security implications before merging.

## Scope

This security policy covers:
- The repository source code and configuration files
- CI/CD pipeline definitions
- Any scripts or tooling in the repository

It does **not** cover the educational content of the handbooks themselves, which are provided for reference only.
