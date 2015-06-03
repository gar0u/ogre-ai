# TODO:
#	1) Make an 'ogre' package, so everything is under one dir (yes)
#	3) Include a copy of mysql-connector
#       4) Test

from distutils.core import setup

setup(name = 'ogre',
      packages = ['ogre', 
                  'mysql.connector', 
                  'mysql.connector.django',
                  'mysql.connector.fabric', 
                  'mysql.connector.locales',
                  'mysql.connector.locales.eng'],
      version = '0.9.1',
      author = 'William J. Hutton, III',
      author_email = 'william.hutton@wsu.edu',
      maintainer = 'William J. Hutton, III',
      maintainer_email = 'williamhutton@gmail.com',
      description = 'Python implementation of OGRE.',
      long_description = 'Python modules that implement the classic OGRE\n' + \
                         '     board game for using artificial intelligence\n' + \
                         '     algorithms to explore the game.',
      platforms='Any',
      data_files =  [('/usr/local/ogre', ['main'])],
      scripts = ['scripts/ogre.sql'],
      license = 'No license',
      url = 'None',
      classifiers = ['Programming Language :: Python', 
                     'Programming Language :: Python :: 3',
                     'License :: No license',
                     'Operating System :: OS Independent',
                     'Development Status :: Alpha'],
)
