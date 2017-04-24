# 
seq2pkl converts xml score into the following format to make it easier to load and save by using `pickle`

[(instrument, [(pitch, dynamic, rhythmValue, duration),...]), ...]
namely, [part, ...] where part = (instrument, [note, ...])

**NOTICE**: this is for xmls which have been processed by xml2seq/xml2seq2. Not wise to process initial xmls with this.
