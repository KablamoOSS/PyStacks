formatters = {
    'RED': '\033[91m',
    'GREEN': '\033[92m',
    'END': '\033[0m',
}


def boxwrap(text, linenumbers=True):
    '''Wraps text in a box'''
    response = ''
    text = text.encode('utf-8')

    split = text.splitlines()
    if len(split) == 0:
        return response

    total = max([len(x) for x in split])
    if linenumbers:
        total += 7
    else:
        total += 3

    response = '+' + ('-' * total) + '+' + '\n'

    for index, line in enumerate(text.splitlines()):
        if linenumbers:
            newline = '| {index}. {line}'.format(index=index + 1, line=line)
        else:
            newline = '| {line}'.format(index=index + 1, line=line)

        if len(newline) < total:
            newline += ' ' * (total - len(newline) + 1)
            newline += '|'

        response += newline + '\n'

    response += '+' + ('-' * total) + '+'
    return response


def writecolour(text, colour='RED'):
    response = '{' + colour + '}' + text + '{END}'
    response = response.format(**formatters)
    return response


def whalesay(text):
    response = boxwrap(text=text, linenumbers=False)
    response += '''
\
            \                ==
             \              ===
       /""""""""""""""""\___/ ===
      {                      /
       \______ o          __/
         \    \        __/
          \____\______/'''
    return response


def piesay(text):
    response = boxwrap(text=text, linenumbers=False)
    response += '''

             (
              )
         __..---..__
     ,-='  /  |  \  `=-.
    :--..___________..--;
     \.,_____________,./  '''
    return response
