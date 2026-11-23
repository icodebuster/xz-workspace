# Axis-Sonar

Local SonarQube analysis of `../Axis-ERP` (Simon's Axis code), kept in its own
folder so `Axis-ERP` stays an untouched copy of `main`. Nothing is ever
written into `Axis-ERP`'s tracked files.

This folder is tracked in the workspace repo, so it reaches every Mac with a
`git pull`. Kept out of git (see the workspace `.gitignore`): `.env.sonar` (the
token), `Gemfile.lock` (rebuilt on every run) and `reports/`.

## Day to day

```sh
git -C ../Axis-ERP pull          # Simon's latest (never conflicts: nothing here edits it)
bin/sonar up                     # only if the server isn't running (OrbStack must be)
bin/sonar scan                   # gems, tests with coverage, RuboCop, Brakeman, analysis
bin/sonar open                   # dashboard: http://localhost:9000/dashboard?id=xzibit-axis
```

From Claude Code (in a session started in `Xzibit_Workspace/`), `/scan-code`
does all of this and reports the results; `/scan-code pull` updates Axis-ERP
first, and `/scan-code --skip-tests` is the quick version.

`bin/sonar scan --skip-tests` reuses the last coverage; `--system` adds the
system tests (needs Chrome). `bin/sonar help` lists everything.

## What's here

| File | What it does |
| --- | --- |
| `bin/sonar` | Every command. Runs Ruby inside `Axis-ERP`, with this folder's Gemfile |
| `compose.yml` | The server: SonarQube Community Build plus its own Postgres, on 127.0.0.1 only |
| `sonar-project.properties` | What's analysed, excluded, and left out of coverage (paths relative to `Axis-ERP`) |
| `Gemfile` | `Axis-ERP`'s Gemfile plus SimpleCov |
| `Gemfile.lock` | Copy of `Axis-ERP`'s lock, refreshed on every run, plus SimpleCov |
| `coverage.rb` | Starts SimpleCov before Rails, instead of editing `test_helper.rb` |
| `.env.sonar` | `SONAR_HOST_URL` and the analysis token. Owner-only, never share |
| `reports/` | Output of each run: `coverage/` (open `coverage/index.html`), `rubocop.json`, `brakeman.json`, scanner work files |

## How it leaves Axis-ERP alone

- **Gems:** `Axis-ERP`'s lock doesn't list this Mac's platform, so using its
  own Gemfile could make Bundler rewrite `Gemfile.lock`. Every Ruby command
  runs with `BUNDLE_GEMFILE` pointing here instead, and the lock here starts as
  a copy of `Axis-ERP`'s, so the gem versions are exactly `main`'s.
- **Coverage:** the tests run as `ruby -rbundler/setup -r coverage.rb bin/rails test`,
  so SimpleCov starts before the app loads, with no edit to `test_helper.rb`.
- **Output:** reports go to `reports/` here. The test run's own `log/` and
  `tmp/` files in `Axis-ERP` are ones its `.gitignore` already ignores.
- **Analysis:** the scanner reads the settings file here and treats `Axis-ERP`
  as the project root, so file paths and git blame are the real ones.

`AXIS_DIR=/path/to/another/checkout bin/sonar scan` analyses a different copy.

## Server and history

The compose project is `axis-sonarqube`, the same name the old
`Vendor/LaunchAssembly/Axis` copy used, so it's the same server with every
earlier analysis. The history lives in Docker volumes, not in any folder, so
deleting the old copies of the code doesn't lose it. Project key `xzibit-axis`,
quality gate "Sonar way" (judges code changed in the last 30 days).

- `bin/sonar down` stops it, keeping everything. `bin/sonar logs` follows its log.
- Starting over (deletes every analysis and the admin password):
  `docker compose -f compose.yml down -v`, delete `.env.sonar`, then
  `bin/sonar up` and `bin/sonar setup`.
- Upgrading: back up first
  (`docker compose -f compose.yml exec db pg_dump -U sonar sonar > sonarqube-backup.sql`),
  then change the pinned `sonarqube:` tag in `compose.yml` and run `bin/sonar up`.

## On another Mac (the Mac mini)

This folder comes with the workspace repo, but the server and its history
don't: they live in Docker on the Mac that ran `bin/sonar up`. A second Mac
gets its own server, with its own history, set up once:

```sh
git -C ~/_Work/Xzibit/40_Code/Xzibit_Workspace pull
brew install sonar-scanner                          # and OrbStack, if it isn't there
rbenv install -s $(cat ../Axis-ERP/.ruby-version)   # run from Axis-Sonar/
bin/sonar up                                        # first boot takes a few minutes
bin/sonar setup                                     # new admin password, project, token -> .env.sonar
bin/sonar scan                                      # or /scan-code in Claude
```

`bin/sonar setup` asks for passwords, so run it in your own terminal, not
through Claude.

## Troubleshooting

- **`rbenv: version ... is not installed`**: Simon moved Ruby.
  `rbenv install -s $(cat ../Axis-ERP/.ruby-version)`, then scan again.
- **`401` from the scanner**: the token in `.env.sonar` was revoked or is for
  another server. `bin/sonar setup` makes a new one.
- **PDF tests fail with `Errno::ENOENT` in `Pdfs::ChromeRenderer`**: no
  Chrome found on this Mac. **`uninitialized constant Vips::Image`**:
  `brew install vips`. Either way coverage is still counted from the other tests.
- **"Invalid character encountered in ... emails/ingestor.rb"**: that file
  holds a U+FFFD character on purpose. Harmless.
- **"External issues were imported with a deprecated format"**: Brakeman's
  Sonar format. Still imported; nothing to do.
