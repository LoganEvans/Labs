from __future__ import print_function

def cprint(msg, color='blue'):
    code = dict(zip(['black', 'red', 'green', 'yellow', 'blue',
                     'magenta', 'cyan', 'white'],
                    range(30, 38)))
    print("\033[1;{code}m{msg}\033[0m".format(msg=msg, code=code[color]))


def cstr(msg, color='blue'):
    code = dict(zip(['black', 'red', 'green', 'yellow', 'blue',
                     'magenta', 'cyan', 'white'],
                    range(30, 38)))
    return "\033[1;{code}m{msg}\033[0m".format(msg=msg, code=code[color])


if __name__ == '__main__':
    cprint('blue')
    cprint('red', color='red')
    cprint('green', color='green')
    cprint('magenta', color='magenta')
    cprint('yellow', color='yellow')
    cprint('cyan', color='cyan')
