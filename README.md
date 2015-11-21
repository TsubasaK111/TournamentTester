# TournamentTester
My version of Udacity's Full Stack Nanodegree "Tournament" project(P2).

This backend database program  is a good boilerplate for coding a
tournament match functionality in your app. It has all of the logic
necessary to manage a tournament in the popular "Swiss Tournament" style.

##Installation:
  1. **Install all requirements.**
  2. Download the contents of this repo.
  3. Open command prompt.
  4. Enter `cd [directory of your choice] && python tournament_init.py`
  5. Some console messages should print, ending with "Success! All tests pass!"
  6. You may now run any of the functions inside `tournament.py`
  7. Profit!

##Requirements:
  * <a href="https://www.python.org/downloads/">Python2</a>
  * <a href="http://www.postgresql.org/">PostgreSQL</a>
  * <a href="http://www.sqlalchemy.org/"> SQLAlchemy</a>
<br>
<br>(_Alternatively_, if you run vagrant and git, you can just:<br>
`git clone https://github.com/udacity/fullstack-nanodegree-vm.git fullstack`<br>
and `vagrant up`.)

##Issues:
  Scaffolding script in `tournament_init.py` fails and halts when 'tournament'
  database already exists. If the database already exists, the script should
  continue to create/replace tables and test database functionality in the
  preexisting database.

###Todo:
  Make script continue if database already exists.

##License:
  TournamentTester is distributed under the <a href="http://opensource.org/licenses/MIT">MIT License</a>.
