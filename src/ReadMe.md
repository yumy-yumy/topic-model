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

2.2. Build a vocabulary by running

`python ldaPy/vocabulary.py -f all_text.txt -o all_term.dat`,

in which `all_term.dat` is the file saving the vocabulary.
Please write down the total number of terms because you will need it in the step 3.1.

2.3. Convert the data to the format required by the model, which means each line is in the form of 

[the number of unique terms] [term_1]:[count] [term_2]:[count] ...  [term_N]:[count].

Type

`ldaPy/mult.py -f /home/text/text_1998.txt -t all_term.dat -o /home/mult/foo-mult-1998.dat`,

where `/home/text/text_1998.txt` is the text file of year 1998 and `/home/mult/foo-mult-1998.dat` is the output. 

Use the shell scripts to process files in the `/home/text` in batch mode by

`./shell/batch_data.sh /home/text /home/mult all_term.dat`,

where the first parameter is the directory of text files; the second one is the output and the last one is the vocabulary.

2.4. Calcuate topic_num and alpha parameter.

Generate sequences of topic numbers for every year by

`python ldaPy/topic_num_seq.py -f stat.csv -o /home/topic_num`,

where `stat.csv` is created in step 1.2.
The folder `/home/topic_num` contains a set of .csv files and they are named as `topic_num_xxxx.csv`, for example `topic_num_1998.csv`.
And each line in the .csv file is in the format of `[topic_num] [alpha]`.

2.5. Train LDA [Blei-Lab/lda-c](https://github.com/Blei-Lab/lda-c).

Train for once by

`lda est [alpha] [topic num] [settings] [/home/mult/foo-mult-1998.dat] [random/seeded/manual=filename/*] [/home/lda_model/1998]`.

Train several models by

`./shell/batch_train.sh /home/mult /home/topic_num /home/lda_model`,

where the first parameter is the output of step 2.3; the second one is obtained in step 2.4 and the last one is the path of the output.

The output is a set of folders named by years, and each of them contains a set of models corresponding to different topic numbers. You are expected to see a set of folders named as `ldac_output_X`, where `X` represents the level of model; in particular, the zero means the lowest level in the tree of hierachy topic graph and the largest number is the topmost level. 


# 3. Computing distances and extracting topics

3.1. Read topic distributions from `final.beta` in the step 2.5.
Run

`python ldaPy/read_prob.py -f /home/lda_model/1998/ldac_output_0/final.beta -o /home/lda_model/1998/prob/prob_0.pkl`

, which reads the probability matrix from `/home/lda_model/1998/ldac_output_0/final.beta` and saves it to `/home/lda_model/1998/prob/prob_0.pkl`.

Run

`python ldaPy/convert_prob.py -f /home/lda_model/1998/prob/prob_0.pkl -n 15591 -o /home/lda_model/1998/prob/convert_prob_0.pkl`,

which adjuts the shape of the matrix.
The second parameter is the size of the vocabulary, probably you need change it.

In the batch mode which also combines these two steps together, use

`shell/prob.sh /home/lda_model /home/topic_num`,

where the first parameter is the result of the step 2.5 and the second one is the folder from the step 2.4.
The script creates a folder named `prob` under each model directory and put results there.

3.2. Obtain topics.

Run

`python graph/topic_term.py -f /home/lda_model/1998/prob/prob_0.pkl -t /home/all_term.dat -o /home/lda_model/1998/topic_0.pkl`,

which stores a list of topics represented by its top 5 terms.

In the batch mode, use

`shell/topic.sh /home/lda_model /home/all_term.dat`.

Similarly in the step 3.1, it creates a folder `topic` under each model and put results there.

3.3. Compute distances between topics.
Run

`python graph/compute_distance.py -f /home/lda_model/1998/prob/convert_prob_0.pkl -g /home/lda_model/1998/prob/convert_prob_1.pkl -o distance_0_1.pkl`.

The output is a distance matrix where each element (i,j) represents the distance between topic i to topic j.

In the batch mode, for dynamic time graph, use

`shell/distances.sh /home/lda_model /home/dtm`,

which computes topics in the topmost level from two different years and saves results in `/home/dtm/distance`.

For hierarchy topic graph, use

`shell/distance.sh /home/lda_model`,

it creates a folder `topic` under each model and save results there.

# 4. Count topics of categories

4.1. Read document topic distributions from `final.gamma` in the step 2.5.
Similar to the step 3.1, type

`python ldaPy/read_prob.py -f /home/lda_model/1998/ldac_output_2/final.gamma -o /home/infer/prob_1998.pkl`.

In the batch mode, use

`shell/infer_prob.sh /home/lda_model /home/infer`,

where the first paramter is the folder cotains models and the second is the output path.
Here, we use models of the topmost level from all years. For example, in 1998, the topmost model is saved in the folder `/lda_model/1998/ldac_output_2`.

4.2. Build a dictionary to transalte categories' short names to their full names.
For arxiv-category, type

`python classification/arxiv_category_dict.py -f /home/class_topic/arxiv_category.txt -o /home/class_topic/arxiv-category_dict.pkl`.

For acm-class, type

`python classification/acm_class_dict.py -f /home/class_topic/acmccs98-1.2.3.xml -o /home/class_topic/acm-class_dict.pkl`.

The output is a file in extension .pkl which contains a dictionary whose keys are categories' short names and values are their full names.

4.3. Get category information of documents.

For arxiv-category, type the command,

`python classification/set_classification.py -f /home/text/text_1998.txt -r /home/data/data_1998.txt -c arxiv-category -o /home/class_topic/arxiv-category/arxiv-category_1998.txt`,

where `-f` is the text file in the step 1.2;
`-r` is the data file containing both category information and texts in the step 1.1;
`-c` is the name of classification system i.e. arxiv-category or acm-class,
`-o` is the output path.

For acm-class, type

`python classification/set_classification.py -f /home/text/text_1998.txt -r /home/data/data_1998.txt -c acm-class -d /home/class_topic/acm-class_dict.pkl -o /home/class_topic/acm-class/acm-class_1998.txt`,

where paramters are similar to those for arxiv-category but we need an extra one `-d` representing the dictionary of categories in the step 4.2.

The output is a file in extension .pkl contains a dictionary whose keys are textes of articles and values are their correspoding categories.

In the batch mode,  use

`shell/set_classification.sh /home/text /home/data /home/class_topic/arxiv-category`.

The first parameter is the directory contains text files;
the second one is the directory contains data files;
the third one is the output directory;
and for acm-class, we need the forth paramter which is the dictionary of categories.

4.4. Count topics of categories for all years.
For arxiv-category, type

`python classification/topic_of_class.py -p /home/infer -m /homde/lda_model -f arxiv-category -c /home/class_topic/arxiv-category -d /home/class_topic/arxiv-category_dict.pkl -o /home/class_topic/class_topic_arxiv-category.pkl`, 

where `-p` is the directory contains posterior distributions in the step 4.1;
`-m` is the directory contains models in the step 2.5;
`-f` is the name of classification system i.e. arxiv-category or acm-class;
`-c` is the directory contains category information of articles in the step 4.3;
`-d` is the dictionary of classification system;
`-o` is the filename recording the output.

The output is a two-level dictionary which is in the format of dict[year][category_name]=[a list of topics], and the topics in the list are repeatable.

BTW, the autohr strongly recommends using shell scripts as they make life easier.
