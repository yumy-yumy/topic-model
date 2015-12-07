`backend` is the backend of the web application.

`graph, ldaPy, preprocess` are used to generate the topic model data to be visualized by the web application and they are independent of `backend`.

This is the tutorial about how to generate the topic model data.

# 1. Preprocessing
1. The raw data is assumed to be a .xml file contains all articles.
In the terminal, type `python preXml.py -f raw_data.xml -o /home/data`, where `raw_data.xml` is the file contains raw data and  `/home/data` is the outpath to save results.
It extracts necessary informartion such as abstract and category of an atrticle and the output is a set of .txt files where each of them contains extracted data in the same year. 

2. There may exit duplicate articles 
`preprocess/preTxt.py` remove duplicate articles

# Training LDA Model

1. `ldaPy/vocabulary.py` build a vocabulary
2. `ldaPy/mult.py` convert documents to the format required by the model
3. `ldaPy/topic_num_seq.py` create a sequence of topic nums for htm
4. train LDA [Blei-Lab/lda-c](https://github.com/Blei-Lab/lda-c)
5. collect results of LDA (extract final.other, final.gamma and final.beta from outputs)

# Drawing Graphs

1. `ldaPy/read_prob.py` & `ldaPy/convert_prob.py` save results from .beta and .gamma to .pkl files and convert shape of matrix(so that in the future we do not have to read these large files again and again)
2. `graph/top_term.py` obtain top terms of topics
3. `graph/compute_distance.py` compute distances between topics
4. `backend/graph.py` draw graph
5.  `graph/topic_of_class.py` count topics of each category for all years










