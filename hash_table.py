def intersect(list1, list2):
  """Return a set with every element in both lists, no duplicates"""
  return set(list1).intersection(list2)

# Word list
def hash_table():
    """Creates hash table where each index is the list of all words with that character in that position"""
    with open("sgb-words.txt", "r") as tf:
        words = tf.read().split('\n')

    words_upper = []

    for w in words:
        words_upper.append(w.upper())

    hash_table = [[[] for width in range(26)] for height in range(5)]


    def hashfunc(word):
        """Adds each word to the hash_table"""
        for position in range(5):
            letter_index = ord(word[position]) - ord('A')
            hash_table[position][letter_index].append(word)

    for word in words_upper:
        if len(word) == 5:
            hashfunc(word)

    return hash_table

final_hash_table = hash_table()

poss_sols = set([])
for row in range(5):
  for col in range(26):
    for word in final_hash_table[row][col]:
      poss_sols.add(word)
# print(poss_sols[0])

print(chr(ord('A')+1))

