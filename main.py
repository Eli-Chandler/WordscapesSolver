# Dictionary credits:
# 1000 words: https://gist.github.com/deekayen/4148741
# 10,000 words: https://github.com/first20hours/google-10000-english
# All words: https://github.com/dwyl/english-words


class LetterNode():
    is_word = False
    def __init__(self, letter):
        self.letter = letter
        self.child_letters = dict()

dictionaries = ['top1000.txt', 'top10000.txt', 'all.txt']

def read_word_list(node, filename):
    with open(filename) as f:
        while word := f.readline().strip():
            if len(word) > 7:
                continue
            curr = node
            for i, char in enumerate(word):
                if char not in curr.child_letters:
                    curr.child_letters[char] = LetterNode(char)
                curr = curr.child_letters[char] # update current node to the node we just made
                if i == len(word) - 1:
                    curr.is_word = True



def traverse(node, letter_counts, curr_word = ""):
    for char, count in letter_counts.items():
        if count > 0 and char in node.child_letters:
            new_counts = letter_counts.copy()
            new_counts[char] -= 1
            traverse(node.child_letters[char], new_counts, curr_word+char)
    if node.is_word:
        if curr_word not in tried_words and len(curr_word) in word_counts and word_counts[len(curr_word)] > 0:
            tried_words.add(curr_word)
            while True:
                worked = input('Is ' + curr_word + ' one of your words? (y/n): ')
                if worked == 'y':
                    word_counts[len(curr_word)] -= 1
                    break
                if worked == 'n':
                    break

counts = {
    's': 1,
    'o': 1,
    'l': 1,
    'i': 1,
    'd': 1
}

word_counts = {
    3: 5,
    4: 4,
    5: 1
}

tried_words = set()

for d in dictionaries:
    if sum(word_counts.values()) > 0:
        root = LetterNode(None)
        read_word_list(root, d)
        traverse(root, counts)


