#!/usr/bin/env python
# Scaffolding script to make tournament database operational.
# Execute this script before running tournament.py or tournament_test.py!

import subprocess
import tournament_test

try:
    create_database_output = subprocess.check_output(
                            "psql -c 'CREATE DATABASE tournament;'", shell=True)
    print("SUCCESS! create_database_output returned:")
    print(create_database_output)
except:
    print("EXCEPTION! create_database_output returned:")
    print(create_database_output)
    pass

try:
    tournament_sql_output = subprocess.check_output(
                            "psql -f tournament.sql", shell=True)
    print("SUCCESS! tournament_sql_output returned:")
    print(tournament_sql_output)
except:
    print("EXCEPTION! tournament_sql_output returned:")
    print(tournament_sql_output)
    pass

tournament_test.testAll()
