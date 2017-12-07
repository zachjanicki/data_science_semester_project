# task 5 w/ keyword table instead of entity table

import sqlite3
from fim import apriori, fpgrowth

def extract_data(db):
    command = 'SELECT keyword, paper_id from Keywords'
    output = db.execute(command)
    transactions = {}
    for t in output:
        if t[0] not in transactions:
            transactions[t[1]] = [t[0]]
        else:
            transactions[t[1]].append(t[0])

    list_tran = []
    for t in transactions:
        list_tran.append(transactions[t])

    return list_tran

if __name__ == '__main__':
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    transactions = extract_data(c)
    print 'loaded data'
    apriori_patterns = apriori(transactions, supp=-7)
    print '-------- Apriori --------'
    output = []
    for (pattern,support) in sorted(apriori_patterns,key=lambda x:-x[1]):
        if len(pattern) > 1:
            print pattern,support
    print 'Number of patterns:',len(apriori_patterns)