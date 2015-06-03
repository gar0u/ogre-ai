INSTALLATION INSTRUCTIONS

1. Unpack the source file:
   (You already did this or you would not be reading this file!)  =)

   $ tar -xvzf ogre-#-#-#.tar.gz

2. Enter the source directory:

   $ cd ogre-#-#-#

3. Run the 'setup.py' script:  

   $ python3 setup.py install

4. Create the MySQL objects by running './scripts/ogre.sql':
   (May require escalated privileges or at least database
    administrator credentials.)

   $ mysql -u root -p mysql < ./scripts/ogre.sql

5. Run the command-line script to have the computer play 'n'
   games of OGRE against itself.

   E.g. To play 5 games of OGRE, use the following command:

   $ /usr/local/ogre/main -n 5

   If there is enough training data in the database (currently
   100 games), the computer will use a genetic algorithm to
   try and improve its performance against the OGRE.  Otherwise
   it will randomly select and place units on the board according
   to the rules.

   Units can be BRAVE, DISCIPLINED, or COWARDLY, which effects
   how each unit moves and fires.  (Due to time constraints,
   only BRAVE units are implemented in this version.)

NOTES:

a. Most modules have a 'DEBUG = False' value near the top of the file
   that can be set to 'True' to generate more verbose output if you
   are interested in that sort of thing.

   Some interesting files to try this on would be;

   i)   '/usr/local/ogre/main'  (This module contains the main game loop.)
   ii)  'ogre.py'               (This module controls OGRE fire/move turns.)
   iii) 'unit.py'               (This module controls defender units.)
   iv)  'crt.py'                (This module implements the Combat Result Table.)

b. If you would like to generate your own training data, simply;

   i)   Log into MySQL:

        $ mysql -u ogre -p ogre
        ogrepw (N.b. password will be masked and not appear when you type.)

        It takes about 1m 30s to simulate 100 games.  (Most of the overhead
        is from several database commits.  Without MySQL logging, the
        system can play 100 games in about 20s.)

    ii) Truncate all the simulation generated data;

        > TRUNCATE TABLE Games;
        > TRUNCATE TABLE Units;
        > TRUNCATE TABLE Ogres;

    Then rerun the simulation.  You can also adjust various constants
    to adjust the behavior of the simulation, including the
    probabilities that randomly generated units will be homegeneous
    or heterogeneous, the probability of a genetic mutation in the
    algorithm, now many training games are required before the
    genetic algorithm begins learning, etc.
