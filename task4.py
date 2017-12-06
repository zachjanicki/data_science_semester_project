import sqlite3
from itertools import chain, combinations

def extract_data(db, min_sup):
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

        # count the number of times each author shows up
        if t[2] not in authors:
            authors[t[2]] = 1
        else:
            authors[t[2]] += 1

    ##########################################
    counter = 0
    for a in authors:
        print '{}: {}'.format(a, authors[a])
        counter += 1
        if counter > 10:
            break
    counter = 0
    for t in transactions:
        print '{}: {}'.format(t, transactions[t])
        counter += 1
        if counter > 10:
            break
    ##########################################

    return transactions, authors

    # remove all papers that only have one author
    '''
    for author in authors:
        if authors[author] == 1:
            authors.pop(author, None)
    '''

def powerset(iterable):
    s = list(iterable)
    a = chain.from_iterable(combinations(s, r) for r in range(1, 3))
    counter = 0
    output = []
    for i in a:
        counter += 1
        if len(i) > 1:
            output.append( (str(i[0]), str(i[1])) )
    print counter
    print len(output)
    return output

def set_size_one(authors, transactions, min_sup):
    C1 = authors
    L1 = {}
    for a in C1:
        if C1[a] >= min_sup:
            L1[a] = C1[a]
    print 'size of author set {}'.format(len(L1))
    
    # get rid of papers with less than 2 authors for the next function
    for k, v in transactions.items():
        if len(v) < 2:
            del transactions[k]
    print 'size of transaction set: {}'.format(len(transactions))
    return L1, transactions

def set_size_two(L1, transactions, min_sup):
    C2 = []
    L2 = powerset(L1)
    collab_dict = {}
    for item in L2:
        for t in transactions:
            if item[0] in transactions[t] and item[1] in transactions[t]:
                if item in collab_dict:
                    collab_dict[item] += 1
                else:
                    collab_dict[item] = 1

    # get rid of papers with less than 3 authors for the next function
    for k, v in transactions.items():
        if len(v) < 3:
            del transactions[k]
    print 'size of transaction set: {}'.format(len(transactions))

    return collab_dict, transactions


def set_size_three(authors, L2, transactions, min_sup):
    L3 = {}
    print 'length of author set: {}'.format(len(authors))
    for entry in L2:
        for author in authors:
            if author not in entry and L2[entry] > min_sup:
                for t in transactions:
                    if entry[0] in transactions[t] and entry[1] in transactions[t] and author in transactions[t]:
                        if (entry[0], entry[1], author) not in L3:
                            L3[(entry[0], entry[1], author)] = 1
                        else:
                            L3[(entry[0], entry[1], author)] += 1
    
    # get rid of papers with less than 4 authors for the next function
    for k, v in transactions.items():
        if len(v) < 4:
            del transactions[k]
    print 'size of transaction set: {}'.format(len(transactions))
    return L3, transactions

def set_size_four(authors, L3, transactions, min_sup):
    L4 = {}
    for entry in L3:
        for author in authors:
            if author not in entry:
                for t in transactions:
                    if entry[0] in transactions[t] and entry[1] in transactions[t] and entry[2] in transactions and author in transactions[t]:
                        if (entry[0], entry[1], entry[2], author) not in L3:
                            L4[(entry[0], entry[1], entry[2], author)] = 1
                        else:
                            L4[(entry[0], entry[1], entry[2], author)] += 1
    return L4, transactions


if __name__ == '__main__':
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    min_sup = 12
    transactions, authors = extract_data(c, min_sup)
    L1, transactions = set_size_one(authors, transactions, min_sup)
    for key in L1:
        print key, L1[key]
    L2, transactions = set_size_two(L1, transactions, min_sup)
    for key in L2:
        print key, L2[key]
    L3, transactions = set_size_three(authors, L2, transactions, min_sup)
    for key in L3:
        print key, L3[key]
    L4, transactions = set_size_four(authors, L3, transactions, min_sup)
    for key in L4:
        print key, L4[key]



