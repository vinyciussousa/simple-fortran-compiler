output_file = None

def open_file(filename):
    global output_file
    output_file = open(filename, 'w')

def write_to_file(content):
    global output_file
    output_file.write(content + '\n')

def close_file():
    global output_file
    if output_file:
        output_file.close()