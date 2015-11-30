# Dynamic Time Graph (dtm)

Dynamic time graph is designed to discover how topics change over time.

Input: a set of documents

Output: a data structure encoding graph

Algorithm:

1. Set a constraint on Hellinger distance Hmax.
2. Group data by year.
3. For each year, compute a reasonable topic num based on the number of documents and then train LDA to obtain topic distributions.
4. For two adjacent years (i, j), for each pair of topics (p, q) from i, j, calculate Hellinger distance H(p, q).
   If H(p, q) is smaller than Hmax, add a link between them.


# Hierachy Topic Graph (htm)

It is a tree where topics on upper levels are parent topics to those on lower levels.

Input: a set of documents published in the same year

Output: a data structure encoding the tree

Alogrithm:

1. Compute a set of reasonable topic numbers based on the number of documents.
2. For each topic num, train LDA to obtain topic distributions.
3. For each topic from level i, calculate its Hellinger distance to all topics in its uppler level(i+1) and then set the topic with the minimum distance as its parent node.


# Dynamic Time Graph of Category
