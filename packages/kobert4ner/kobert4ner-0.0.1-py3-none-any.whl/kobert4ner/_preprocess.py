import re

def preprocess(raw_text):
    # join all lines
    text = re.sub('\s',' ',raw_text)
    
    # split by the ends of sentences
    # ex) . ! ?
    text = re.split('(?<=[\!\?\.][ ])', text)
    
    # split sentence by non-alphanumeric
    text = [re.split('[^\w]',sent) for sent in text if sent and not sent.isspace()]
    
    return [[word for word in sent if word] for sent in text]