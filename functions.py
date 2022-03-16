# Read player position (from string to tuple)
def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

# Make player position (from tuple to string)
def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])