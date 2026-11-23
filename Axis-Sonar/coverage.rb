# Line coverage for SonarQube, without editing Axis-ERP's test_helper.rb.
# bin/sonar runs the suite as `ruby -rbundler/setup -r<this file> bin/rails test`,
# so SimpleCov starts before the app loads and everything in app/ is counted.
# SimpleCov 1.x follows the parallel test workers' forks and merges them.
# SonarQube reads coverage.json; index.html is for people.
require "simplecov"

SimpleCov.coverage_dir ENV.fetch("SONAR_COVERAGE_DIR")
SimpleCov.start "rails"
