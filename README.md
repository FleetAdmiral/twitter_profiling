# twitter_profiling
In this project, we aimed to create vector representations of twitter profiles by analysing two paramenters:
1) Hashtags used by the user in his posts
2) The accounts that the user follows

To run the above file, you'll need to download the following:
1) Custom dataset, that we scraped. Please mail or text one of us to get the same.
2) The pre-trained Google Word2Vec corpus: https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit

twitter_profiling.py - the main file that does the making of the vector, imports htseparator to split hashtags and then get a representation of the split hashtags to add to the user vector.
