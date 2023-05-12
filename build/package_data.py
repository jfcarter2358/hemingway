files = ['data/data.json', 'data/frequencies.json', 'data/punctuation.json', 'data/rules.json']
names = ['data', 'frequencies', 'punctuation', 'rules']

output = ''

for idx, path in enumerate(files):
    with open(path, 'r', encoding='utf-8') as data_file:
        contents = data_file.read()

    contents = contents.replace(': true', ': True')
    contents = contents.replace(': false', ': False')

    output += f'{names[idx]} = {contents}\n\n'

with open('hemingway/data.py', 'w', encoding='utf-8') as output_file:
    output_file.write(output)
