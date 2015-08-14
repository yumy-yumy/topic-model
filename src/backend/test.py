import topic
import ioFile

if __name__ == "__main__":
    
    graph_data = topic.topics_for_year(1993)
    graph_data = topic.topics_from_to(1993, 1999)
    graph_data = topic.topics_for_class("A.1", 1998, 2001)
    #ioFile.save_json(graph_data, "graph.json")