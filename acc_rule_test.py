# need to be run from orange3 virtual environment
from orangecontrib.associate.fpgrowth import *
from Orange.data.sql.table import *

# get the SQL table
conn = {'host':'wifitracking.bk.tudelft.nl', 'port':5432, 'dbname':'wifi', 'user':'team2', 'password':'AlsoSprachZ!'}
table = SqlTable(conn,'buildingset_v0504_test',inspect_values=True)

data, mapping = OneHot.encode(table, include_class=True)
itemsets = dict(frequent_itemsets(data, .02))

sorted(mapping.items())

class_items = {item for item, var, _ in OneHot.decode(mapping, table, mapping) if var is table.domain.class_var}

rules = [(P, Q, supp, conf) for P, Q, supp, conf in association_rules(itemsets, .7)]

names = {item: '{}={}'.format(var.name, val) for item, var, val in OneHot.decode(mapping, table, mapping)}
for ante, cons, supp, conf in rules[:5]:
    print(', '.join(names[i] for i in ante), '-->',names[next(iter(cons))],'(supp: {}, conf: {})'.format(supp, conf))

