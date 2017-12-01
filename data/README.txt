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
    AUD
    AUT


DB schema
=========

Tables - Papers, Authors, Keywords

Papers
    PAPER_ID
    TITLE
    YEAR
    PAPER_TEXT

Authors
    AUTHOR_ID
    AUTHOR_NAME
    PAPER_ID

Keywords
    KEYWORD
    PAPER_ID
    CONFIDENCE
