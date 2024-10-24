# Changelog

This file includes a history of past releases. Changes that were not yet added to a release are in the [changelog.d/](./changelog.d) folder.

<!--
⚠️ DO NOT ADD YOUR CHANGES TO THIS FILE! (unless you want to modify existing changelog entries in this file)
Changelog entries are managed by scriv. After you have made some changes to this plugin, create a changelog entry with:

    scriv create

Edit and commit the newly-created file in changelog.d.

If you need to create a new release, create a separate commit just for that. It is important to respect these
instructions, because git commits are used to generate release notes:
  - Modify the version number in `__about__.py`.
  - Collect changelog entries with `scriv collect`
  - The title of the commit should be the same as the new version: "vX.Y.Z".
-->

<!-- scriv-insert-here -->

<a id='changelog-19.0.0'></a>
## v19.0.0 (2024-10-23)

- 💥[Feature] Upgrade to Sumac. (by @Faraz32123)
- [BugFix] Uwsgi workers wasn't starting properly using `UWSGI_WORKERS` flag, passing the value directly fixes the issue. (by @Faraz32123)
- 💥[Feature] Update Credentials Image to use Ubuntu `24.04` as base OS. (by @Faraz32123)
  - Add `mime-support` alternatives that are `media-types mailcap`.
  - Update `python-openssl` to `python3-openssl`.
- [Bugfix] Fix legacy warnings during Docker build. (by @regisb)


<a id='changelog-18.0.0'></a>
## v18.0.0 (2024-06-07)

- 💥[Feature] Upgrade to Redwood. (by @Faraz32123)
- [Feature] Add `atlas pull` at build-time. (by @omarithawi)
- [Bugfix] Make plugin compatible with Python 3.12 by removing dependency on `pkg_resources`. (by @regisb)
- [Feature] Make it possible to use mounts for a local development. (by @cmltawt0)
- [BugFix] Fix award program certificates error. (by @rohan-saeed)
- 💥[Feature] Upgrade Python version to 3.11.9. (by @Faraz32123)
- [BugFix] Fix custom image pull/push. (by @dyudyunov)

<a id='changelog-17.0.1'></a>
## v17.0.1 (2024-01-23)

- [Bugfix] Fix initialization tasks in production. (by @Danyal-Faheem)

<a id='changelog-17.0.0'></a>
## v17.0.0 (2023-12-09)

- 💥[Feature] Upgrade to Quince. (by @ Talha-Rizwan)
- [Feature] Add support for the Learner Record MFE. (by @arbrandes)

<a id='changelog-16.1.0'></a>
## v16.1.0 (2023-11-30)

- [Improvement] Added Typing to code, Makefile and test action to the repository and formatted code with Black and isort. (by @CodeWithEmad)
- [Bugfix] Fix build error due to outdated nodeenv. (by @regisb)
- [Bugfix] Added missing default configs that were missed during merge. (by @Faraz32123)
- 💥[Improvement] Simplify plugin settings. As a consequence, many marketing settings are deprecated. If they were useful to you, you can override them using the "credentials-settings-common" patch. (by @regisb)

<a id='changelog-16.0.3'></a>
## v16.0.3 (2023-11-21)

- [Bugfix] Fix the issue of site was not being created during tutor dev launch. (by @Faraz32123)
- [Enhancement] Add support for using custom credentials repository using CREDENTIALS_REPOSITORY and CREDENTIALS_REPOSITORY_VERSION. (by @Faraz32123)
- [Documentation] Add command for creating credentials superuser in the readme. (by @Faraz32123)

<a id='changelog-16.0.2'></a>
## v16.0.2 (2023-11-08)

- [BugFix] Corrected variable name for installing pip extra requirements. (by @Faraz32123)

<a id='changelog-16.0.1'></a>
## v16.0.1 (2023-10-24)

- [BugFix] Reorder staticfiles command in Dockerfile to resolve the Missing staticfiles manifest entry for 'bundles'. (by @hinakhadim)

<a id='changelog-16.0.0'></a>
## v16.0.0 (2023-06-15)

- [Improvement] Add a scriv-compliant changelog. (by @regisb)

- 💥[Feature] Upgrade to Palm. (by @Faraz32123)

## Version 14.0.0 (2022-09-15)

* general production release for nutmeg.master

## Version 0.0.3 (2022-09-14)

* bump to nutmeg.master
* rebuild Dockerfile based on openedx and license_manager

## Version 0.0.2 (2022-09-13)

* run user sync after migrations
* remove any parameters that can be defaulted with existing Tutor params
* create_dot_application(s)
* set ALLOWED_HOSTS and SECRET_KEY


## Version 0.0.1 (2022-05-28)

**Experimental. Do not use in production.**

* Initial Git import
