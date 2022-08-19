

# Word list
def hash_table():
    with open("sgb-words.txt", "r") as tf:
        words = tf.read().split('\n')

    words_upper = []

    for w in words:
        words_upper.append(w.upper())

    hash_table = [[] for size in range(130)]


    def hashfunc(word):
        for letter_index in range(5):
            table_index = ord(word[letter_index]) - ord('A')
            table_index += letter_index * 26
            hash_table[table_index].append(word)

    for i in words_upper:
        if len(i) == 5:
            hashfunc(i)

    return hash_table

final_hash_table = hash_table()

print(final_hash_table[0])
