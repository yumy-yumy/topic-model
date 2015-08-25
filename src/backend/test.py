import topic
import ioFile

if __name__ == "__main__":
    
    topic_tree = topic.topics_for_year(1998)
    ioFile.save_json(topic_tree, 'tree.json')