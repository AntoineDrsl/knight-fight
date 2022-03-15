# Read player position
def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

# Make player position
def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])