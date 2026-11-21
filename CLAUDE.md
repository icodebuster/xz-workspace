# Xzibit_Workspace

This folder holds the Axis repos side by side so one Claude session can work across them. The folder itself is a small git repo (`icodebuster/xzibit-workspace`) that tracks only this file, `.claude/settings.json`, `.gitignore`, `repos.txt`, `setup.sh`, `README.md`, `Xzibit_Workspace.code-workspace` and `.vscode/settings.json`. Each project folder is its own git repo, ignored here, with its own `CLAUDE.md`, which loads when Claude first reads a file in that folder.

Each folder's own `CLAUDE.md` is the authority for that folder. This file is only the map and the cross-folder rules: never copy a folder's rules up here, point to them.

## The folders

| Folder | What it is | Repo | Claude may |
|---|---|---|---|
| `Axis-ERP/` | Axis source (Rails), built by Simon (Launch Assembly) | `xzibit-apps/Axis-ERP` | Read only. Never edit, commit or push |
| `Axis-Docs/` | PRDs and the Axis Confluence space. JK works on the `JK-WIP` branch; Joel's work is the `Joel-WIP` branch of this same repo | `xzibit-apps/Axis-Docs` | Write, following `Axis-Docs/CLAUDE.md` and the `prd-writer` skill |
| `Axis-UI-Testing/` | Playwright UI tests for axis-dev | `icodebuster/Axis-UI-Testing` | Write and run, following its Rules section |
| `Axis-UI-Reference/` | Axis UI prototype (Vue) and UI kit: the reference for expected UI | see `repos.txt` | Read only unless asked |
| `WhipIT/` | WhipIT 3 tooling, Atlas and WhipIT to Axis migration docs | `icodebuster/xz-whipit` | Write, following `WhipIT/CLAUDE.md` |
| `_handoff/` | Files passed between folders (route lists, change summaries, test summaries) | not in git | Write. Nothing secret, no client details |

## Before acting in a folder

- Read that folder's `CLAUDE.md` rules first. The hard ones, in short (the folder's file has the detail):
  - `WhipIT/`: scripts hit PRODUCTION unless `WHIPIT_ENV=dev`. One request at a time, no retries, big pulls only after 5pm Brisbane or at weekends.
  - `Axis-UI-Testing/`: plain `npm test` is safe. Saving runs only on axis-dev, picked with `--case` or `--screen`. Never email a quote.
  - `Axis-Docs/`: change files with Edit and Write only, never shell commands. Publish with `/publish-confluence`, never copy and paste.
- Never read or print `.env` files, `.auth/`, or anything holding a password or token, in any folder.
- Never use the em dash character in any file or reply. Use a hyphen, comma, colon or parentheses.

## Axis-ERP

There is one copy of Simon's code, `Axis-ERP/`. No repo here holds it as a submodule; WhipIT reads it as `../Axis-ERP`. WhipIT's migration docs record the Axis commit they were read from: check what changed since with `git -C Axis-ERP fetch` and then `git -C Axis-ERP log --oneline <commit>..`.

`Axis-ERP/CLAUDE.md` is very large (about 3,800 lines) and is excluded from automatic loading in this workspace (`.claude/settings.json`). When a task needs Simon's conventions or domain rules (stages, roles, quoting, timesheets), list its `## ` headings with grep and read only the sections needed.

## Starting a session

- **Cross-folder work** (code to tests, code to docs, WhipIT data into tests or docs): start Claude in `Xzibit_Workspace/`.
- **Work inside one folder** (a long test-building session, PRD writing): start Claude inside that folder. Its own `.claude/settings.json` (permissions, hooks such as the doc-name check in `Axis-UI-Reference/`) only applies when the session starts there. This file still loads, because Claude reads `CLAUDE.md` files in parent folders.

## Cross-folder workflows

### New feature from Simon -> UI tests
1. In `Axis-ERP/`, find the routes and forms for the feature (`config/routes.rb`, the controllers and views). Note the commit (`git -C Axis-ERP log -1 --oneline`).
2. Write `_handoff/routes-<feature>-<YYYY-MM-DD>.json`: `[{ "name": "...", "url": "...", "notes": "..." }]`, with the commit in the first entry's notes.
3. In `Axis-UI-Testing/`, add or update scenario files as its `CLAUDE.md` describes (`npm run inventory` for the page list), compare against `Axis-UI-Reference/` where a look is checked, then dry run.

### Bring Joel's changes into Axis-Docs
1. `git -C Axis-Docs fetch origin Joel-WIP`. Never pull or merge it into the current branch without asking.
2. `git -C Axis-Docs diff HEAD...origin/Joel-WIP --stat`, then the diff of each file of interest (three dots: only what Joel changed since the branches split). Read a whole file of his with `git -C Axis-Docs show origin/Joel-WIP:"<path>"`.
3. Write a summary to `_handoff/joel-changes-<YYYY-MM-DD>.md` and ask which changes to bring across.
4. Apply the agreed changes in `Axis-Docs/` on `JK-WIP` with Edit and Write, following its PRD lifecycle rules.

### WhipIT data for tests or docs
Run WhipIT scripts from inside `WhipIT/` (they resolve paths from the repo root), on dev unless JK asks for production. Exports stay in `WhipIT/data/` (git-ignored, live business data); copy into `_handoff/` only structure or counts, never client names or contact details.

## Git across the repos

`git bulk` (git-extras, workspace name `xzibit`, registered by `setup.sh`) runs one git command in every repo here, for example `git bulk -w xzibit fetch` or `git bulk -w xzibit status`. Never use it for commit, push, pull, merge or reset: those are done in one repo at a time, and only when asked.

## Machines

This workspace is used on JK's MacBook and a Mac mini, both at `/Users/JK/_Work/Xzibit/40_Code/Xzibit_Workspace`. Secrets (`.env` files, `.auth/`, Keychain entries) and Claude's own session history stay on each machine. The Axis-UI-Testing 8:15 am nightly run is on the MacBook only: never run `npm run nightly:on` on the Mac mini.
