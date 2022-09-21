#!/usr/bin/python3

import random
import argparse
from datetime import datetime
import os.path
import shutil


test_run = False

def testprint(*args, **kwargs):
    if test_run:
        print(*args, **kwargs)


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


@run_once
def init_random():
    testprint("Initializing random")
    random.seed()


# Reads the topics from the topics file and returns a list of topic Dics
def load_topics(topics_file_name):
    # Load the opics from disk
    with open(topics_file_name) as topics_file:
        # Holds dictionaries of topics. The a topic Dictionary holds the actual
        # line in the topics file and the topic string.
        topics = []

        # A topics file is a csv file. The first line of the topics files is 
        # not a topic, but rather the csv headers. Read the first line and 
        # throw it away, then read the next line, which will be the first topic.
        topics_file.readline()
        line = topics_file.readline().strip()
        cur_file_line = 2
        while line:
             
            # If the topic is unused, the line starts with the letter 'N', for 
            # Not Used, then add it to the topics list.
            if line[0] == 'N':
                topics.append({'line_in_file' : cur_file_line, 'topic' : line.split(',')[1]})
                
            # read in the next topic
            line = topics_file.readline().strip()
            cur_file_line += 1
    return topics



# Returns a Dic of the random topic
def get_random_topic(topics):
    if len(topics) > 0:
        init_random()
        ri = random.randrange(0, len(topics))
        return topics[ri]
    else:
        return None


def mark_topic_as_used(file_name, topic):
    line_in_file = topic['line_in_file']
    testprint("Marking line " + str(line_in_file) + " as used")

    with open(file_name, "r") as topics_file:
        for x in range(0, line_in_file - 1):
            line = topics_file.readline()

        write_loc = topics_file.tell()
        testprint("read to location " + str(write_loc))

    with open(file_name, "r+") as topics_file:
        testprint("writing to location " + str(write_loc))
        topics_file.seek(write_loc)
        topics_file.write("Y")

    with open("topic_history.txt", "a") as used_topics:
        now = datetime.now()
        used_topics.writelines(now.strftime("%m/%d/%Y %H:%M:%S")+ ": " + topic['topic'] + "\n")
 

def tests(topics):
# pick a random unused topic
#    num_tries = 1
#    ri = random.randint(0, len(topics) - 1)
#    while ri != len(topics) - 1:
#        num_tries += 1
#        ri = random.randint(1, len(topics) - 1)

#    print("It took", num_tries, "tries to randomly get", len(topics) - 1)


#    get_topic_x_for_test(topics, 1)
    #for x in range(len(topics)):
#    print(topics[0])
#    print(topics[1])
#    for x in range(2, len(topics) + 1):
#        get_topic_x_for_test(topics, x)

    for x in range(0, len(topics)):
        #print("Topic", x, topics[x])
        get_topic_x_for_test(topics, x)

       
def get_topic_x_for_test(topics, x):
    print("get_topic_x_for_test looking for topic:", x)
    topic = get_random_topic(topics)
    tries = 1
#    while topic['line_in_file'] != x:
    while topic != topics[x]:
        #print("Matching", x, "against", topic['line_in_file'])
        topic = get_random_topic(topics)
        tries += 1
    print("Took", tries, "to find topic", x, topic) 


def main():
    working_topics_file = 'working_topics.txt'
    initial_topics_file = 'initial_topics.txt'
    if os.path.exists(working_topics_file) == False:
        if os.path.exists(initial_topics_file):
            shutil.copyfile(initial_topics_file, working_topics_file)
        else:
            print("No topics file found")
            return
    
    topics = load_topics(working_topics_file)
    testprint("Found " + str(len(topics)) + " topics")

    if test_run == True:
        tests(topics)

    topic = get_random_topic(topics)
    if topic == None:
        print("No topics found")
        return

    testprint(topic)
    
    print("\n"+topic['topic']+"\n")

    mark_topic_as_used(working_topics_file, topic)



if __name__ == "__main__":
    main()

