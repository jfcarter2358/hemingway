import hemingway.pos
from nltk.corpus import brown
from pprint import pprint

if __name__ == '__main__':
    correct = 0
    wrong = 0
    error_report = {}
    total = len(brown.categories())
    for index, category in enumerate(brown.categories()):
        print(f'Parsing Brown category {category}, {index+1} of {total}...')
        sents = brown.tagged_sents(categories=category, tagset='universal')
        sent_total = len(sents)
        print(f'    Processing sentence 1 of {sent_total}...')
        for sent_index, sent in enumerate(sents):
            if (sent_index + 1) % 100 == 0:
                print(f'    Processing sentence {sent_index+1} of {sent_total}...')
            tokens = [token[0] for token in sent]
            tagged = hemingway.pos.tag_tokens(tokens)

            for idx, part in enumerate(tagged):
                if part[1] == sent[idx][1]:
                    correct += 1
                else:
                    key = f'{part[1]} | {sent[idx][1]}'
                    if not key in error_report:
                        error_report[key] = 1
                    else:
                        error_report[key] += 1
                    wrong += 1
            

    total = correct + wrong
    percent_correct = (correct / total * 100)
    percent_wrong = (wrong / total * 100)
    
    print()
    print('RESULTS')
    print('--------')
    print(f'Correct: {percent_correct:.2f}% | {correct}')
    print(f'Wrong  : {percent_wrong:.2f}% | {wrong}')
    print()
    # pprint(sorted(error_report.items(), key=lambda x:x[1]))
