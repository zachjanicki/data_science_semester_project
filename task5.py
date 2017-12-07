# task 5
import sqlite3
from fim import apriori, fpgrowth

def extract_data(db):
    command = 'SELECT paper_id, term, count, type FROM Entities WHERE type = "METHOD" or type = "DATASET" or type = "PROBLEM"'
    output = db.execute(command)
    transactions = {}
    problems = []
    methods = []
    datasets = []
    counter = 0
    for entry in output:
        counter += 1
        if entry[0] not in transactions:
            transactions[entry[0]] = []
            for i in range(0, int(entry[2])):
                transactions[entry[0]].append(entry[1])
        else:
            for i in range(0, int(entry[2])):
                transactions[entry[0]].append(entry[1])
        if entry[3] == 'PROBLEM':
            problems.append(entry[1])
        elif entry[3] == 'METHOD':
            methods.append(entry[1])
        elif entry[3] == 'DATASET':
            datasets.append(entry[1])

    print counter

    list_tran = []
    for t in transactions:
        list_tran.append(transactions[t])
    counter = 0
    

    return list_tran, problems, methods, datasets

def generate_associations(transactions, min_sup, problems, methods, datasets):
    apriori_patterns = apriori(transactions, supp=-min_sup)
    print '-------- Apriori --------'
    output = []
    for (pattern,support) in sorted(apriori_patterns,key=lambda x:-x[1]):
        print pattern,support
    print 'Number of patterns:',len(apriori_patterns)

    rules = apriori(transactions,target='r',supp=-5,conf=90,report='sc')
    print '-------- One-to-Many Association Rules --------'
    counter = 0
    for (ruleleft,ruleright,support,confidence) in sorted(rules,key=lambda x:x[0]):
        if ruleleft in datasets:
            for rule in ruleright:
                if rule not in datasets:
                    counter += 1
                    print ruleleft,'-->',ruleright,support,confidence    
        elif ruleleft in problems:
            for rule in ruleright:
                if rule not in problems:
                    counter += 1
                    print ruleleft,'-->',ruleright,support,confidence
        elif ruleleft in methods:
            for rule in ruleright:
                if rule not in methods:
                    counter += 1
                    print ruleleft,'-->',ruleright,support,confidence
        #print ruleleft,'-->',ruleright,support,confidence
    print 'Number of rules:',len(rules)
    print counter


if __name__ == '__main__':
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    transactions, problems, methods, datasets = extract_data(c)
    #print transactions
    generate_associations(transactions, 10, problems, methods, datasets)