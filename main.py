# start out as basic repl
# make lists using !add commands
# !add [listname] [thing to add to list]
# !view [listname]
# !delete [listname] [number]

#TODO make lists choosable by index
#TODO make error handling red and only one line, not stack trace, not crash the program
#TODO separate out the code to different files
#TODO make annotation that registers it into the command database
#TODO exit nicer on kbinterrupt
#TODO define new lists with schemas
#TODO make up arrow key work
#TODO connect to irc something
#TODO make data persistent in some sort of data store

#services to interface
# sms
# email
# stack of todo
# todo
# sheet lists
# calendar / agenda
# wakeup message
# reminders
# torrent client control
# daily vocab word
# file sync interface
# everything

import shelve

def parse_command(line):
    command = "help"
    options = []
    arguments = []
    for word in line.split():
        if word[0] == '!':
            command = word[1:]
        elif word[0] == '-':
            options.append(word[1:])
        else:
            arguments.append(word)
    return (command, options, arguments)

def run_command(command, options, arguments):
    fun = get_function(command)
    print(fun[0](*arguments))

def get_function(name):
    return funcs[name]

def repl(db):
    while True:
        nice = input("> ")
        if not nice:
            continue
        try:
            run_command(*parse_command(nice))
        except KeyError:
            print("%s command not found" % nice)
        except TypeError as e:
            print("ERROR-------------------- %s" % e)

funcs = {}
def register(name, options, nargs):
    def decarator(func):
        funcs[name] = (func, options, nargs)
    return decarator

@register("help", {}, 0)
def print_help():
    return "you are bad HAHAHA"

@register("add", {}, 2)
def add(a, b):
    return float(a) + float(b)

@register("sub", {}, 2)
def sub(a, b):
    return float(a) - float(b)

#TODO make the parser general, as a dictionary with first class functions
@register("list", {"n":1}, 0)
def todo(*args):
    if not args: return lists.keys()
    selected = args[0]
    if len(args) == 1:
        for i,x in enumerate(lists[selected]):
            print('%d -- %s' % (i+1,x))
        return 1
    subcommand = args[1]
    if subcommand == "new":
        lists[args[0]] = list()
        return('created new list: %s' % args[0])
    if args[0] not in lists:
        raise TypeError('unknown list %s' % args[0])
    if subcommand == "add":
        lists[selected].append(" ".join(args[2:]))
        return lists[selected]
    if subcommand == "remove":
        try:
            n = int(args[2])
            del lists[selected][n-1]
        except IndexError as e:
            return "index out of range"
        except ValueError as e:
            return str(e)
        return lists[selected]

    #should never reach
    raise Exception('should never reach')


print(funcs)
with shelve.open('db') as db:
    if 'lists' not in db:
        db['lists'] = {}
    lists = db['lists']
    try:
        repl(db)
    finally:
        db['lists'] = lists
