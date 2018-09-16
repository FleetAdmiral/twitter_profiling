from alphabet_detector import AlphabetDetector
from math import log

WORDS_FILE = 'words.txt'

class HTS:
    def __init__(self):
        words = open(WORDS_FILE).read().split()
        # Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability)
        self.WORDCOST = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))
        self.MAXWORD = max(len(x) for x in words)
    
    def split(self, s):
        s = s.lower()

        # Find the best match for the i first characters, assuming cost has
        # been built for the i-1 first characters
        # Returns a pair (match_cost, match_length)
        def best_match(i):
            candidates = enumerate(reversed(cost[max(0, i-self.MAXWORD):i]))
            return min((c + self.WORDCOST.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)

        # Build the cost array
        cost = [0]
        for i in range(1,len(s)+1):
            c,k = best_match(i)
            cost.append(c)

        # Backtrack to recover the minimal-cost string
        out = []
        i = len(s)
        while i>0:
            c,k = best_match(i)
            assert c == cost[i]
            out.append(s[i-k:i])
            i -= k

        s = " ".join(reversed(out))
        return(s, list(reversed(out)))

if __name__=='__main__':
    print('''
    USAGE:
        hts=HTS()
        print(hts.split(<HASHTAG>))

    NOTE:
        <HASHTAG> should not contain the # symbol at the beginning

    Example:
        "garbagehuman" = 
    ''')

    hts = HTS()
    print(hts.split('garbagehuman'))