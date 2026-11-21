# xzibit-workspace

The workspace that holds JK's Axis repos side by side, so one Claude Code session (or one VS Code window) can work across them.

This repo tracks only the workspace's own files:

| File | Purpose |
|---|---|
| `CLAUDE.md` | The map of the folders and the cross-folder rules Claude follows |
| `.claude/settings.json` | Workspace-wide Claude Code settings (secret files never read, Axis-ERP never edited, Axis-ERP's large CLAUDE.md not loaded automatically) |
| `repos.txt` | The project repos and the folder name each is cloned into |
| `setup.sh` | Clones what is missing and registers `git bulk` |
| `.gitignore` | Keeps the project repos, `_handoff/` and machine-only files out of this repo |
| `Xzibit_Workspace.code-workspace`, `.vscode/settings.json` | The VS Code workspace: every repo as its own root |

The project folders (`Axis-ERP`, `Axis-Docs`, `Axis-UI-Testing`, `Axis-UI-Reference`, `WhipIT`) are separate repos and are git-ignored here, as is `_handoff/`.

## Set up on a new Mac

```sh
mkdir -p /Users/JK/_Work/Xzibit/40_Code
cd /Users/JK/_Work/Xzibit/40_Code
git clone git@github.com:icodebuster/xzibit-workspace.git Xzibit_Workspace
cd Xzibit_Workspace
brew install git-extras        # once per Mac, for git bulk
./setup.sh
```

Then do the by-hand steps `setup.sh` prints (secrets and installs). Keep the same path on every Mac: some CLAUDE.md files use absolute paths.

## Every day

```sh
git bulk -w xzibit fetch       # fetch every repo
git bulk -w xzibit status      # what has changed where
```

Open the workspace in VS Code with File > Open Workspace from File > `Xzibit_Workspace.code-workspace`, and start Claude in the `Xzibit_Workspace` folder for work that spans folders.
