# start out as basic repl
# make lists using !add commands
# !add [listname] [thing to add to list]
# !view [listname]
# !delete [listname] [number]

#TODO make error handling red and only one line, not stack trace
#TODO separate out the code to different files

def parse_command(line):
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
    return shut[name]

def add(a, b):
    return int(a) + int(b)

def repl():
    while True:
        nice = raw_input("> ")
        try:
            run_command(*parse_command(nice))
        except KeyError:
            raise TypeError("no command found, bad")

shut = {"add":(add, "", 2), "what":()}
repl()
