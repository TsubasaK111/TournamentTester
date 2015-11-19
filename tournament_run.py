#!/usr/bin/env python
# Scaffolding script to make tournament database operational.
# Execute this script before running tournament.py or tournament_test.py!

import subprocess

create_database_output = subprocess.check_output("psql -c 'CREATE DATABASE tournament;'", shell=True)

if create_database_output == """ERROR:  database "tournament" already exists""":
    print("NOTICE: database 'tournament' already exists,"
          "continuing database setup with current dataset...")
else:
    print("create_database_output returned:")
    print(create_command_output)

run_tournament_sql_output = subprocess.check_output("psql -f tournament.sql", shell=True)

print("run_tournament_sql sez:")
print(run_tournament_sql)
