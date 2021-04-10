import wikipedia

wikipedia.set_lang('ru')


def search_wiki(word):
    print(word)
    try:
        w = wikipedia.search(word)
        if w:
            w2 = wikipedia.page(word).url
            # print(w2)
            w1 = wikipedia.summary(word)
            return w1, '\nИсточник:' + w2
        return 'Запрос не найден', ''
    except Exception:
        return 'Запрос не найден', ''
