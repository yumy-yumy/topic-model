# Preprocessing

1. extract necessary informartion and group data by year
preXml.py
input: a .xml file
output: several .txt files by year, where each line is formatted by [category/id/...]\t[text]\n

2. remove duplicates
preTxt.py
input: a .txt file
output: a .txt file only containing text and without duplicates
batch mode:txt.sh

# Training LDA Model

1. build a vocabulary
dtm/dtm_vocabulary.py
input: a .txt file contains all data
output: a all_term.dat file contains all terms

2. convert documents to the format required by the model
dtm/dtm_mult.py
input: a .txt file contains text & all_term.dat
output: a foo-mult.data contains the modeling data
batch mode:batch_data.sh

3. create a sequence of topic nums
graph/topic_num_stat.py
input: a .csv file contatins numbers of documents for each year
output: a list of .csv file contains topic nums and inital values of the alpha parameter

4. train LDA
link to LDA codes: https://github.com/Blei-Lab/lda-c
batch mode:batch_train.sh

5. collect results by LDA
extract final.other, final.gamma and final.beta from outputs

# Drawing Graphs

1. save results from .beta and .gamma to .pkl file and convert shape of matrix(so that in the future we do not have to read these large files again and again)
ldaPy/read_prob.py
input: a .txt file 
output: a .pkl file contains the original matrix and a .pkl file contains the converted one

2. obtain top terms of topics
graph/top_term.py
input: a .pkl file contains topic distributions and a .dat file represents the vocabulary
output: a .pkl file contains a list of topics
batch mode:topic.sh

3. compuate distances between topics
graph/compute_distance.py
input: two .pkl file contains topic distributions for two years
output: a .pkl file contains the matrix of distances
batch mode:distance.sh(htm), distances.sh(dtm)

4. draw graph
backend/graph.py








