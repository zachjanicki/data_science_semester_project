import sqlite3
from fim import apriori, fpgrowth

def extract_data(db):
    command = 'SELECT paper_id, author_id, author_name FROM Authors'
    output = db.execute(command)
    cleaned_output = []
    counter = 0
    for o in output:
        cleaned_output.append([o[0], o[1], o[2]])
        #cleaned_output.append([o[0], o[1], ''.join(i for i in o[2] if ord(i)<128)])
        counter += 1
    print counter
    transactions = {}
    authors = {}
    
    for t in cleaned_output:
        # paper_id is the key for each transaction and list(author_name) is the value
        if t[0] not in transactions:
            transactions[t[0]] = [t[2]]
        else:
            transactions[t[0]].append(t[2])
    list_tran = []
    for t in transactions:
        list_tran.append(transactions[t])
    return list_tran

def run_apriori(transactions, min_sup, author_number):
    apriori_patterns = apriori(transactions, supp=-min_sup)
    print '-------- Apriori --------'
    output = []
    for (pattern,support) in sorted(apriori_patterns,key=lambda x:-x[1]):
        if len(pattern) < author_number:
            continue
        print pattern,support
        output.append([pattern, support])
    print 'Number of patterns:',len(apriori_patterns)
    return output



if __name__ == '__main__':
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    transactions = extract_data(c)
    print 'data extracted'
    
    f_two_authors = open('data/2_author_collaborations.txt', 'w')
    output = run_apriori(transactions, min_sup=10, author_number=2)
    for line in output:
        f_two_authors.write(str(line) + '\n')
    
    output = run_apriori(transactions, min_sup=6, author_number=3)
    f_three_authors = open('data/3_author_collaborations.txt', 'w')
    for line in output:
        f_three_authors.write(str(line) + '\n')

    output = run_apriori(transactions, min_sup=3, author_number=4)
    f_four_authors = open('data/4_author_collaborations.txt', 'w')
    for line in output:
        f_four_authors.write(str(line) + '\n')




