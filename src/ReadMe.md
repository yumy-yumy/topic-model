`backend` is the backend of the web application.

`graph, ldaPy, preprocess` are used to generate the topic model data to be visualized by the web application and they are independent of `backend`.

This is the tutorial about how to generate the topic model data.

# 1. Preprocessing

1.1. The raw data is assumed to be a .xml file contains all articles.

In the terminal, type 

`python preprocess/preXml.py -f raw_data.xml -o /home/data` 

, where `raw_data.xml` is the file contains raw data and  `/home/data` is the path to save results.
It extracts necessary informartion such as abstract and category of an atrticle.
The output is a set of .txt files where each of them contains extracted data in the same year.
In the .txt file, each line represents an article by the format of [id]\t[text].
You may need modify the code to extract exactly what you want and be careful of the order of elements.

1.2. We then need extract texts from .txt files in step 1.2. Also there may exist duplicate articles and they should be removed. 

Run 

`python preprocess/extract_text.py -f data_1998.txt -o /home/text`

, where `data_1998.txt` is the input .txt file containing articles in 1998 and similary, `/home/text` is the output path.
The output is a `text_1998.txt` file only contains texts of articles without duplicates. 
A `stat.csv` file is created if it does not exist and a line in the format of `[1998] [the number of articles]` is added to this file.

To run it in batch mode, use the shell script by

`./shell/text.sh /home/data /home/text`,
 
 where the first parameter is the input directory and the second one is the output directory.

# 2. Training LDA Model

2.1. Create a .txt file contains articles of all years. For Linux, run

`cat /home/text/* > all_text.txt`,

where `/home/text` is the output in the step 1.2 which contains a set of text files.
Be cautious, you need move `/home/text/stat.csv` out of the folder `/home/text` at first.

2.2 Build a vocabulary by running

`python ldaPy/vocabulary.py -f all_text.txt -o all_term.dat`,

in which `all_term.dat` is the file saving the vocabulary.

2.3. Convert the data to the format required by the model, which means each line is in the form of 

[the number of unique terms] [term_1]:[count] [term_2]:[count] ...  [term_N]:[count].

Type

`ldaPy/mult.py -f /home/text/text_1998.txt -t all_term.dat -o /home/mult/foo-mult-1998.dat`,

where `/home/text/text_1998.txt` is the text file of year 1998 and `/home/mult/foo-mult-1998.dat` is the output. 

Use the shell scripts to process files in the `/home/text` in batch mode by

`./shell/batch_data.sh /home/text /home/mult all_term.dat`,

where the first parameter is the directory of text files; the second one is the output and the last one is the vocabulary.

2.4 Calcuate topic_num and alpha parameter.

Generate sequences of topic numbers for every year by

`python ldaPy/topic_num_seq.py -f stat.csv -o /home/topic_num`,

where `stat.csv` is created in step 1.2.
The folder `/home/topic_num` contains a set of .csv files and they are named as `topic_num_xxxx.csv`, for example `topic_num_1998.csv`.
And each line in the .csv file is in the format of `[topic_num] [alpha]`.

2.5. Train LDA [Blei-Lab/lda-c](https://github.com/Blei-Lab/lda-c).

Train for once by

`lda est [alpha] [topic num] [settings] [/home/mult/foo-mult-1998.dat] [random/seeded/manual=filename/*] [/home/lda_model/1998]`.

Train several models by

`./shell/batch_train.sh /home/mult /home/topic_num /lda_model`,

where the first parameter is the output of step 2.3; the second one is obtained in step 2.4 and the last one is the path of the output.

The output is a set of folders name by years, and each of them contains a set of models corresponding to different topic numbers. You are expected to see a set of folders named as `ldac_output_X`, where `X` represents the level of model; in particular, the zero means the lowest level in the tree of hierachy topic graph and the largest number is the topmost level. 


# 3, Computing distances and extracting topics

1. `ldaPy/read_prob.py` & `ldaPy/convert_prob.py` save results from .beta and .gamma to .pkl files and convert shape of matrix(so that in the future we do not have to read these large files again and again)
2. `graph/top_term.py` obtain top terms of topics
3. `graph/compute_distance.py` compute distances between topics
4. `backend/graph.py` draw graph
5.  `graph/topic_of_class.py` count topics of each category for all years










