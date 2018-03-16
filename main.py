# start out as basic repl
# make lists using !add commands
# !add [listname] [thing to add to list]
# !view [listname]
# !delete [listname] [number]

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

def repl():
    while True:
        nice = raw_input("> ")
        if not nice:
            continue
        try:
            run_command(*parse_command(nice))
        except KeyError:
            raise TypeError("%s command not found" % nice)
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
lists = {"movies": ['toy story']}
@register("list", {"n":1}, 0)
def todo(*args):
    if not args: return lists.keys()
    if args[0] == "new":
        lists[args[1]] = list()
        print('created new list: %s' % args[1])
    else:
        if args[0] not in lists:
            raise TypeError('unknown list %s' % args[0])
        selected = args[0]
        if len(args) == 1:
            for i,x in enumerate(lists[selected]):
                print('%d -- %s' % (i+1,x))
            return 1
        subcommand = args[1]
        if subcommand == "add":
            lists[selected].append(" ".join(args[2:]))
            return lists[selected]
    return args


print(funcs)
repl()
