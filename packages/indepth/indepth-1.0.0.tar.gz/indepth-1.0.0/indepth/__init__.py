
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Invoke Libraries
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
import pandas as pd
import os
import warnings
from indepth.functions import remov_punct, symSentSim  

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Main function
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# for a pair of document and query, the top sentences with high symmetric sentence similarity are returned.
def MostSimilarSent(d, q, num_sents):
    lcase = d.lower()
    sentences = lcase.split('.')
    if(num_sents > len(sentences)):
        warnings.warn("num_sents is more than the total number of sentences in the document. Hence num_sents is set to total number of sentences.")
    q = remov_punct(q)
    SSSlist = [(s, symSentSim(s,q)) for s in sentences if s]
    df = pd.DataFrame(SSSlist,columns = ['sentence','SSScore'])
    sorted_df = df.sort_values(['SSScore'],ascending=False)
    maxSimSents = sorted_df.head(num_sents)
    return(maxSimSents)