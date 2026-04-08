# baseliner

## problem statement

there are many tools that can be used to scan repositories for various types of metadata and compliance with certain policies, but there is no simple, flexible tool that can be used as a starting point for more complex tools in the future. This tool is intended to fill that gap by providing a simple, flexible tool that can be used to scan a collection of repositories and determine if they are compliant with a baseline policy/ruleset.

## goal

create a tool that can scan a collection of repositories and determine if they are compliant with a baseline policy/ruleset; this is intended to be a simple tool that can be used as a starting point for more complex tools in the future, but it should be flexible enough to allow for future expansion

## anti-goals

this is not a static analysis tool. it is not a tool for compliance in the sense of legal or regulatory compliance, rather this is directed towards (internal) operational and process compliance within a software development context. it is not a code formatter or linter. it is not a tool for enforcing code style or similar, although it could be used to enforce structural conventions. it is not meant as a check on a specific repository - it is meant to be used _on_ repositories, but it is not meant to be used _for_ repositories in the sense of being a tool that is run as part of a CI/CD pipeline or similar; rather, in theory it would live in its own repository with its configuration file(s) and workflow(s) and doc(s).

## scope

### near-term (mvp)

-

### mid-term (v1.0 - personal / internal use)

-

### long-term (v2.0+ - public release)

-

### out of scope (never to be done in this project)

-

## state of the art / literature review:

- **Dependabot** is GitHub’s native dependency automation tool. It can raise pull requests for vulnerable dependencies and version updates, and it can be enabled at the repository or organization level. However, its scope is fundamentally **dependency-centric**; it is not a general repository baseline engine for arbitrary metadata, governance, or cross-platform policy evaluation. ([GitHub Docs][1])

- **Renovate** is a broader dependency update bot that can be self-hosted and applied across many repositories. It supports centralized/self-hosted configuration and repository onboarding, so it is closer than Dependabot to a fleet-wide tool. Still, its core model is also **dependency management and update PR generation**, not general-purpose repository inspection and baseline compliance across heterogeneous repository properties. ([docs.renovatebot.com][2])

- **OpenSSF Scorecard** evaluates repositories against a set of software supply-chain and security best practices, and **Scorecard Monitor** extends this to organization-level tracking with Markdown/JSON reports and optional GitHub issue alerts. This is highly relevant because it shows that multi-repository automated policy checking is feasible. However, Scorecard is intentionally focused on **security and supply-chain health**, not a flexible, extensible baseline engine for arbitrary repository metadata and future custom rules. ([undefined][3])

- **Semgrep Managed Scans** supports onboarding repositories in bulk across GitHub, GitLab, Bitbucket, and Azure DevOps, including optional auto-scan of current and future repositories. This makes it strong for large-scale code and security scanning. However, it is centered on **static analysis findings in source code**, rather than building a general internal representation of a repository that can combine local file metadata, git metadata, and host-platform metadata under one baseline policy layer. ([Semgrep][4])

- **SonarQube** provides multi-project aggregation through **Applications** and **Portfolios**, giving higher-level views of code quality and releasability across many repositories. This is useful for organization-level visibility, but it remains primarily a **code quality platform**, not a lightweight, platform-agnostic baseline compliance engine intended as a simple foundation for future tooling. ([Sonar Documentation][5])

- **Codacy** also supports organization-level repository monitoring and dashboards for code quality, security posture, and configuration metrics. Like SonarQube, it provides fleet-level visibility, but it is still oriented toward a hosted code analysis product rather than a simple extensible engine for arbitrary repository baseline policies. ([Codacy Docs][6])

- **GitHub-native governance features** now include organization-wide **rulesets**, which can apply rules to multiple repositories, and **GitHub Code Quality**, which provides repository and organization dashboards plus ruleset-based enforcement. These features show that repository-fleet governance is increasingly being pulled into the hosting platform itself. The limitation is that they are **platform-specific**, whereas the proposed tool aims to keep the core engine independent of GitHub so that adapters for GitLab, Codeberg, or local repositories can be added later. ([GitHub Docs][7])

- **Backstage** and **Port** are relevant at a higher layer. Backstage provides a centralized software catalog built around metadata files stored with code, while Port provides scorecards and rule-based standards tracking across catalog entities. These systems are useful as organizational control planes, but they assume a broader developer portal or catalog model. They are not, by themselves, the simple baseline repository scanner proposed here. ([Backstage][8])

- A closely related existing GitHub-specific project is **safe-settings**, which manages repository settings, branch protections, teams, and related organization policy as code from a central admin repository. This is highly relevant because it demonstrates centralized repository governance as code, but it is focused on **GitHub settings enforcement** rather than general baseline scanning over local structure, git history, and remote host metadata. ([GitHub][9])
  - This should be carefully examined to determine if and how we would integrate with or differentiate from it. It may be that safe-settings could be used as a GitHub adapter for enforcing certain rules related to repository settings, while the core engine remains platform-agnostic and extensible.

[1]: https://docs.github.com/en/code-security/concepts/supply-chain-security/about-dependabot-security-updates "About Dependabot security updates"
[2]: https://docs.renovatebot.com/self-hosted-configuration/ "Self-Hosted configuration options - Renovate documentation"
[3]: https://scorecard.dev/ "OpenSSF Scorecard"
[4]: https://semgrep.dev/docs/deployment/managed-scanning/overview "Semgrep Managed Scans"
[5]: https://docs.sonarsource.com/sonarqube-server/user-guide/applications "Using applications | SonarQube Server"
[6]: https://docs.codacy.com/organizations/managing-repositories/ "Managing repositories"
[7]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets "About rulesets - GitHub Docs"
[8]: https://backstage.io/docs/features/software-catalog/ "Backstage Software Catalog and Developer Platform"
[9]: https://github.com/github/safe-settings "github/safe-settings"
[10]: https://docs.github.com/en/code-security/concepts/supply-chain-security/about-dependabot-version-updates "About Dependabot version updates"

## conceptual flow (vision)

- input:
  - collection of repositories (this could be a local directory, a list of git repositories, or a list of GitHub repositories; it could be a certain user or an organization's repositories)
  - baseline policy / ruleset (needs to be simple from start, but should be flexible enough to allow for future expansion; for example, in the future allow for finer-grained rules or layering of rules or similar)
- process:
  - initial scan for each directory to obtain metadata from files (e.g., file structure, artifact typing, LOC, etc.)
  - if its a git repository, also obtain git metadata (e.g., commit history/metrics, branch structure, etc.)
  - if it has a remote (e.g., GitHub), also obtain remote metadata (e.g., PR history/metrics, issue history/metrics, branch protection, deployments, CI/CD, etc.)
  - from this create some kind of internal representation of the repository
  - apply the baseline policy/ruleset to this internal representation to determine if the repository is compliant or not, and if not, what the issues are
- output:
  - report of compliance for each repository (this should be some data structure that can be easily consumed by other tools, e.g., JSON or CSV; we can then built a separate tool to create a human-readable report from this if needed and in the future expand to create determinitistic remediation steps or AI/ML-based remediation suggestions)
