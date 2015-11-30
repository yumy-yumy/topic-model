# Preprocessing

1. `preprocess/preXml.py` extract necessary informartion and group data by year
2. `preprocess/preTxt.py` remove duplicates

# Training LDA Model

1. `ldaPy/vocabulary.py` build a vocabulary
2. `ldaPy/mult.py` convert documents to the format required by the model
3. `ldaPy/topic_num_seq.py` create a sequence of topic nums for htm
4. train LDA [Blei-Lab/lda-c](https://github.com/Blei-Lab/lda-c)
5. collect results of LDA (extract final.other, final.gamma and final.beta from outputs)

# Drawing Graphs

1. `ldaPy/read_prob.py` save results from .beta and .gamma to .pkl files and convert shape of matrix(so that in the future we do not have to read these large files again and again)
2. `graph/top_term.py` obtain top terms of topics
3. `graph/compute_distance.py` compute distances between topics
4. `backend/graph.py` draw graph










