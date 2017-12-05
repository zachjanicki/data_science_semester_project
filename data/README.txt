All of the data resides in this folder, most of the files and directories are in .gitignore to avoid huge commits

Below are the files in the microsoft.zip folder and the data they contain:

index.txt
    folder name in txt/ 
    PDFID (filename)
    PID
    TITLE

Papers.txt
    PID 
    TITLECASE
    TITLE
    YEAR
    DATE
    DOI
    CONF_FULL_NAME
    CONF
    CID

PaperKeywords.txt
    PID
    KEYWORD
    KID

PaperAuthorAffiliation.txt
    PID
    AID
    FID
    AFF_ORG
    AFF
    SID

Authors.txt
    AID
    AUT

AffilsCleaned.txt
    PID
    AID
    FID
    AFF
    SID

AuthorsCleaned.txt
    NAME
    AID
    PID

DB schema
=========

Tables - Papers, Authors, Keywords, Affiliations

Papers
    PAPER_ID
    TITLE
    YEAR
    PAPER_TEXT

Authors
    AUTHOR_ID
    AUTHOR_NAME

Keywords
    KEYWORD
    PAPER_ID
    CONFIDENCE

Affiliations
    PAPER_ID
    AUTHOR_ID
    SID -- author sequence number
