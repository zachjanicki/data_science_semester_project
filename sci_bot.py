# This is a command line program to run the various SciBot tasks

def main():
    print 'Welcome to SciBot'
    f_read = open('microsoft/Papers.txt')
    f_write = open('Papers_cleaned.txt', 'w')
    CIDs = ['icdm', 'kdd', 'wsdm', 'www']
    papers_kept = 0
    for line in f_read:
        for conf in CIDs:
            words = line.split()
            if conf in line and len(words[0]) == 8: # checking to make sure the first entry is a valid paper ID and belongs to a valid conference
                if conf != 'www':
                    f_write.write(line)
                    papers_kept += 1
                else:
                    www_count = 0
                    for word in words:
                        if word == 'www' or 'WWW':
                            www_count += 1
                    if www_count < 3:
                        f_write.write(line)
                        papers_kept += 1
    print papers_kept
    f_read.close()
    f_write.close()

def main2():
    f_papers_cleaned = open('Papers_cleaned.txt')
    f_papers_cleaned_joined = open('Papers_cleaned_joined.txt','w')
    papers_kept = 0
    for line in f_papers_cleaned:
        line_split = line.split()
        pid = line_split[0]
        f_index = open('microsoft/index.txt')
        for paper in f_index:
            paper_split = paper.split()
            index_pid = paper_split[2]
            if pid == index_pid:
                f_papers_cleaned_joined.write(line)
                papers_kept += 1
        f_index.close()
    print papers_kept
if __name__ == '__main__':
    #main()
    main2()
    print 'string 1' == 'string 1'

