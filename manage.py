from functools import wraps
import sys

commands = {}


# Decorator for custom command
def registry_command(cmd_str):
    def decorate(func):
        commands[cmd_str] = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorate


@registry_command('init_db')
def init_db():
    from public import db
    import main

    user_input = input('Do you want to initialize the database, the operation will clear all the data[y|n]？')
    if user_input.strip() == 'y':
        db.drop_all()
        db.create_all()
        print('Initialized successfully！')


def print_usage():
    print('''
usage: %s <command>

command:
    init_db         initialize the database
    ''' % sys.argv[0])


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print_usage()
        sys.exit(1)
    cmd = sys.argv.pop(0)
    arg1 = sys.argv.pop(0)
    r_func = commands.get(arg1)
    if callable(r_func):
        r_func(*sys.argv)
    else:
        print('遇到了不可能会出现的错误！')
