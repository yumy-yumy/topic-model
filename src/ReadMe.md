# Preprocessing

1. `preXml.py` extract necessary informartion and group data by year
2. `preTxt.py` remove duplicates

# Training LDA Model

1. 'dtm/dtm_vocabulary.py' build a vocabulary
2. 'dtm/dtm_mult.py' convert documents to the format required by the model
3. 'graph/topic_num_stat.py' create a sequence of topic nums
4. train LDA [Blei-Lab/lda-c](https://github.com/Blei-Lab/lda-c)
5. collect results by LDA (extract final.other, final.gamma and final.beta from outputs)

# Drawing Graphs

1. 'ldaPy/read_prob.py' save results from .beta and .gamma to .pkl file and convert shape of matrix(so that in the future we do not have to read these large files again and again)
2. 'graph/top_term.py' obtain top terms of topics
3. 'graph/compute_distance.py' compuate distances between topics
4. 'backend/graph.py' draw graph










