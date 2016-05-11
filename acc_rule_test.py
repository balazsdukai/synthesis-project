# need to be run from orange3 virtual environment
from orangecontrib.associate.fpgrowth import *
from Orange.data.sql.table import *

# create SQL reader

conn = {'host':'wifitracking.bk.tudelft.nl', 'port':5432, 'dbname':'wifi', 'user':'team2', 'password':'AlsoSprachZ!'}
table = SqlTable(conn,'buildingset_v0504_test')




