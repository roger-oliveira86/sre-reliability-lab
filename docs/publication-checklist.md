# Publication checklist

Before creating the public repository:

- [ ] Verify ownership and originality; **do not copy the third-party fork**.
- [ ] Inspect the LICENSE and all files to be committed.
- [ ] Confirm no real emails, tokens, AWS account identifiers, credentials, or internal incidents.
- [ ] Verify unit tests locally (or in CI) and check changes with `git diff --cached`.
- [ ] Confirm all paths are under the new repository, not the old fork.

Before merging the first PR:

- [ ] GitHub Actions green; new workflows need a first verified run.
- [ ] Branch ruleset for `main`: PR required, force-push and delete blocked, no bypass.
- [ ] Secret scanning and Dependabot alerts enabled where available.
- [ ] Workflow token defaults to read only and actions use immutable SHA pins.
- [ ] Readme claims describe only implemented features.

After merge:

- [ ] Update the GitHub profile README to add a link to the new repo.
- [ ] Update the GitHub profile Website URL (user profile setting), not only repository metadata.
- [ ] Keep or archive the fork until no dependencies remain; deletion is irreversible.
