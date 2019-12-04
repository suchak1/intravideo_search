from fuzzywuzzy import process
from controller import Worker

print('Processing data...')
with open('utils/imagenet1000_clsidx_to_labels.txt') as fp:
    choices = [line[line.find("'") : line.find(",")].replace("'", "") for idx, line in enumerate(fp)]


query = input('Please enter a word or two word phrase (sep by a space) to see if it or related words are in the 1000 ImageNet classification labels.\nYour word/phrase: ').strip()

print('_' * 75)
print('Naive Search: Here are the top 5 naive results in the labels:')
naive = process.extract(query, choices)
print(naive)
success = input(f'Satisfied? Is "{naive[0][0]}" a synonym of "{query}"? (y/n)\nYour (y/n) response: ')
if success.strip().lower() == 'y':
    print(f'Excellent, try searching for "{naive[0][0]}" in IntraVideo Search.')
    quit()
print('Okay, working harder...')

print('_' * 75)
w = Worker()
related_words = w.get_related_words(query, delim=' ')
# results = {*process.extract(word, choices) for word in related_words}
results = set()
for word in related_words:
    results.update(set(process.extract(word, choices)))
top_5 = sorted(results, reverse=True, key=lambda x: x[1])[:5]

print('Advanced Search: Here are the top 5 advanced results in the labels.')
print(top_5)
top = top_5[0][0]

print('_' * 75)
print(f'Our best guess is that "{top}" is the best match for "{query}".')
print(f'Try your luck searching for "{top}" in IntraVideo Search.')
