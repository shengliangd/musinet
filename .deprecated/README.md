# tool chain for musinet

## General
mid2xml.sh: ../mid/ -> ../xml/, converts mid to xml
sequentialized(2).sh: ../xml/ -> ../seq/, merges multi phrases to single phrase
xml2pkl.sh: ../seq/ -> ../pkl/, converts xml to pkl for later process
merge.py: ../pkl/ -> ../data.pkl, merge all pkl files to one

To create training dataset, run the scripts above in listed order.
