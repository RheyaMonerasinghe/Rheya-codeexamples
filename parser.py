import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
NP -> N | Det NP | NP PP | Adj NP
VP -> V | VP Adv | NP VP | VP PP | VP Conj VP | VP NP | Adv V
PP -> P NP 
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file

    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()
        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words=[]
    currentword=""
    alphabets=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    for x in range(len(sentence)):
        char=sentence[x]
        char=char.lower()
        if char!=" " and char!=".":
            currentword=currentword+char
        else:
            valid=False
            for x in range(len(currentword)):
                if currentword[x] in alphabets:
                    valid=True
            if valid==True:
                words.append(currentword)
            currentword=""
    return(words)
    


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """


    NPchunks=[]
    for subtree in tree.subtrees():
        if subtree.label()=="NP":
            NPchunks.append(subtree)
    falseNPs=[]
    for x in range(len(NPchunks)):
        testchunk=NPchunks[x]
        for i in range(len(NPchunks)):
            if testchunk in NPchunks[i]:
                falseNPs.append(NPchunks[i])
    for x in range(len(falseNPs)):
        index=NPchunks.index(falseNPs[x])
        NPchunks.pop(index)
    return(NPchunks)
            

if __name__ == "__main__":
    main()
