---
name: scan-code
description: Run the local SonarQube scan of Axis-ERP (Axis-Sonar/bin/sonar scan) and report the results. Use when JK says /scan-code, "scan the code", "run sonar", "run the SonarQube scan", or asks for code quality, coverage or security results for Axis.
argument-hint: "[--skip-tests] [--system] [pull]"
disable-model-invocation: true
---

# Scan Axis-ERP with SonarQube

Runs `Axis-Sonar/bin/sonar scan` against `Axis-ERP/` and reports what it found.
How the setup works is in `Axis-Sonar/README.md`; read it only if something
below fails in a way this file doesn't cover.

Arguments: `$ARGUMENTS`
- `--skip-tests`: reuse the last coverage (fast, about a minute).
- `--system`: include the system tests (needs Chrome).
- `pull`: update Axis-ERP first with `git -C Axis-ERP pull --ff-only`. Without
  `pull`, never pull, fetch-merge or otherwise change Axis-ERP.
Pass the `--` options through to `bin/sonar scan` unchanged. Refuse anything
else and say what's allowed.

## Rules

- Never read, print, source or copy `Axis-Sonar/.env.sonar`. Only check it
  exists (`test -f`). `bin/sonar` reads it itself.
- Never edit anything in `Axis-ERP/`. The scan doesn't need to.
- Don't change SonarQube settings, tokens, quality gates or the admin password.
- Never use the em dash character in the report.

## Steps

Paths below are relative to the workspace root
(`/Users/JK/_Work/Xzibit/40_Code/Xzibit_Workspace`). Use absolute paths in commands.

1. **Preflight**, in one Bash call, and stop with a clear message on the first failure:
   - `test -f Axis-Sonar/.env.sonar`. If it's missing, tell JK to copy the token in
     themselves, or run `Axis-Sonar/bin/sonar setup` in their own terminal (it asks
     for the admin password), and stop.
   - `command -v sonar-scanner`. If it's missing: `brew install sonar-scanner`. Ask first.
   - The Ruby in `Axis-ERP/.ruby-version` is installed (`rbenv versions --bare`). If
     not, say Simon moved Ruby, then run `rbenv install -s <version>` (a few minutes,
     in the background).
   - If `pull` was asked for: `git -C Axis-ERP pull --ff-only`. If it isn't a fast
     forward or the tree is dirty, stop and report; never merge or reset.
   - Show the commit that will be scanned: `git -C Axis-ERP log -1 --format='%h %ad %s' --date=short`.

2. **Server.** `curl -sf http://localhost:9000/api/system/status`. If it isn't `UP`:
   - If `docker info` fails, start OrbStack (`open -a OrbStack`) and wait for
     `docker info` to succeed (up to a minute).
   - Then `Axis-Sonar/bin/sonar up`, which waits until the server is ready.

3. **Scan.** Run it in the background, since a full run takes about four minutes:
   `cd Axis-Sonar && bin/sonar scan <options> > <scratchpad>/sonar-scan-<timestamp>.log 2>&1`.
   Tell JK it's running and roughly how long it takes, then wait for the
   completion notification. Don't poll.

4. **Read the results** from the log and from `Axis-Sonar/reports/`:
   - Tests: the `N runs, N assertions, N failures, N errors` line.
   - Coverage: the `Line coverage:` line.
   - Failing tests: the names under each `Failure:` / `Error:` line, with the
     first line of the error.
   - RuboCop: `ruby -rjson -e 'p JSON.parse(File.read("Axis-Sonar/reports/rubocop.json"))["summary"]'`.
   - Brakeman: the number of entries in `issues` in `Axis-Sonar/reports/brakeman.json`.
   - The quality gate: the `QUALITY GATE STATUS:` line (`PASSED` or `FAILED`).
   - Any `✗` line from bin/sonar, `ERROR` from the scanner, or a `401`.

5. **Report** in a short message:
   - The commit scanned and the dashboard link, http://localhost:9000/dashboard?id=xzibit-axis
   - A small table: tests, coverage, RuboCop offenses, Brakeman warnings, quality gate.
   - Failing tests grouped by likely cause. Known causes on this Mac:
     `Vips::Image` (libvips not installed: `brew install vips`),
     `Errno::ENOENT` in `Pdfs::ChromeRenderer` (no Chrome found). Call anything
     else a possible real failure.
   - If the gate failed, say the scan only prints the verdict and the failed
     conditions are on the dashboard (the gate judges code changed in the last 30 days).
   - If the scan itself failed: what failed and the fix from the Troubleshooting
     section of `Axis-Sonar/README.md`.
   - Compare with the previous run when one is in this conversation (coverage up
     or down, more or fewer failures).

The log stays in the scratchpad; name its full path in the report.
