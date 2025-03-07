s = "test for test"

# Split the string into words
words = s.split()

# Initialize an empty string to store the result
reversed_words = ""

# Iterate through the words in reverse order
for word in reversed(words):
    reversed_words += word + " "

# Strip the trailing space
reversed_words = reversed_words.strip()

print(reversed_words)


