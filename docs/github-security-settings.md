# GitHub Security Settings

Repository maintainers should enable:

- CodeQL Default setup for Rust;
- Dependabot alerts and security updates;
- secret scanning and push protection where available;
- private vulnerability reporting;
- branch protection requiring Rust CI;
- signed commits or vigilant mode and signed release tags where practical.

Do not add an advanced CodeQL workflow while Default setup is active. Review
repository settings before every release because those controls are not stored
entirely in Git.
