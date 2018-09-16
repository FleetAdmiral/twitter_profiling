import csv
import os
import pickle
import htseparator
import gensim

class User:
    id=""
    name=""
    hashtag=""
    following=[]

list_of_users = []

#pickling to save time
if os.path.isfile('pickle_dump'):
    print "a"
    list_of_users = pickle.load(open("pickle_dump", "rb"))
else:
    print "b"
    with open('data.csv', 'r') as users:
        reader = csv.reader(users)
        for row in reader:
            u = User()
            u.id=row[0]
            u.name=row[1]
            u.hashtag=row[2]
            u.following=row[9:]
            list_of_users.append(u)
    del list_of_users[0]
    # count = 0
    # for all in list_of_users:
    #     for all_k in all.following:
    #         if "[ \"" in all_k:
    #             count=count+1
    # print count;

#clean the data
    total_users = len(list_of_users)
    i_n=0
    while i_n<total_users:
        k = len(list_of_users[i_n].following)
        if k==1 or k==2:
            del list_of_users[i_n]
            total_users=total_users-1
        else:
            for m in range(k):
                if "[ \"" in list_of_users[i_n].following[m]:
                    list_of_users[i_n].following[m] = list_of_users[i_n].following[m].replace('[ \"', '')
                if " \"" in list_of_users[i_n].following[m]:
                    list_of_users[i_n].following[m] = list_of_users[i_n].following[m].replace(' \"', '')
                if "\"" in list_of_users[i_n].following[m]:
                    list_of_users[i_n].following[m] = list_of_users[i_n].following[m].replace('\"', '')
                if " ]" in list_of_users[i_n].following[m]:
                    list_of_users[i_n].following[m] = list_of_users[i_n].following[m].replace(' ]', '')
                try:
                    list_of_users[i_n].following[m] =  float(list_of_users[i_n].following[m])
                except ValueError, e:
                        print "error", e, list_of_users[i_n].following
                        print k
            i_n=i_n+1

    pickle.dump(list_of_users, open("pickle_dump", "wb"))

print list_of_users[0].id
print list_of_users[0].following

total_users = len(list_of_users)

all_users = []

count_track = 0
for all in list_of_users:
    print "Add ID"
    print count_track
    if float(all.id) not in all_users:
        all_users.append(float(all.id))
    for all_ok in all.following:
        if all_ok not in all_users:
            all_users.append(all_ok)
    count_track = count_track+1

final_n_users = len(all_users)
#making the one-hot vectors
one_hot = [[0 for x in range(final_n_users)] for y in range(total_users)]

index = 0
for all in list_of_users:
    counti = 0
    print index
    for all_in in all_users:
        if all_in in all.following:
            one_hot[index][all.following.index(all_in)]=1
            counti = counti+1
    index = index+1

# pickle.dump(one_hot, open("one_hot", "wb"))
#
# print "Done"
# print one_hot[0]

hts = HTS()
split_hashes = []

# splitting all hashtags now in order to get their representations

for all in list_of_users:
    this_hash = hts.split(all.hashtag)
    split_hashes.append(this_hash[1])

model = gensim.models.Word2Vec.load_word2vec_format('./model/GoogleNews-vectors-negative300.bin')

#finding joint representations of the hashtag
score_hashes = []
for all in split_hashes:
    repr = model.score(all)
    score_hashes.append(repr)

#forming combined vector
ind = 0
for all in list_of_users:
    one_hot.append(score_hashes[ind])
    ind = ind + 1

#___________________________________________
import numpy as np
from sklearn.decomposition import PCA
one_hot=np.array(one_hot)
pca = PCA(n_components=9000)
pca.fit(one_hot)

#___________________________________________
