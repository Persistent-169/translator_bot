import requests
from bs4 import BeautifulSoup


def translator(word, language):
    t_lang = language[-1:language.rfind('-'):-1][::-1]
    response = requests.get('https://context.reverso.net/translation/' + language + '/' + word,
                            headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        })
    soup = BeautifulSoup(response.text, 'html.parser')
    t_word = soup.find_all(['a', 'div'], {"class": ['translation']})
    words = '*' + t_lang.capitalize() + ' Translations:*\n'
    for i in range(1, len(t_word)):
        words += '`' + t_word[i].text.strip() + '`' + '\n'
    examples = soup.find_all(['span'], {'class': ['text']})
    examples_r = []
    examples_e = []
    for example in examples:
        if 'em' in str(example) and 'rel' not in str(example):
            examples_r.append(example.text.strip() + '\n')
        if 'em' in str(example) and 'rel' in str(example):
            examples_e.append(example.text.strip() + '\n\n')

    examples = []
    for i in range(len(examples_r)):
        examples += ['*' + examples_r[i] + '*']
        examples += ['`' + examples_e[i] + '`']
    examples = '\n*' + t_lang.capitalize() + ' examples:*\n' + ''.join(examples)
    return examples, words


