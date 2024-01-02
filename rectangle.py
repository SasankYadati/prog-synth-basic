import random

rectangle = [1,3,1,4] # rectangle is the program

# constraints
# shrooms should be outside and grass inside
shroom1 = (0,4)
shroom2 = (4,1)
grass1 = (1,1)
grass2 = (3,3)

inside = True
outside = False

# execute program on input
def interpret(program, input):
    T, D, L, R = program
    i, j = input
    return i >= T and i <= D and j >= L and j <= R

assert interpret(rectangle, grass1) == inside
assert interpret(rectangle, grass2) == inside
assert interpret(rectangle, shroom1) == outside
assert interpret(rectangle, shroom2) == outside


# specification is a list of input output examples
spec = [(grass1, inside), (grass2, inside), (shroom1, outside), (shroom2, outside)]
shroom3 = (2,2)
grass3 = (4,3)
shroom4 = (5,4)
spec2 = [(shroom3, outside), (grass3, inside), (shroom4, outside)]

# check if program satisfies the spec
def is_correct(program, spec):
    for input, output in spec:
        if interpret(program, input) != output:
            return False
    return True


def random_writer(spec):
    T, D, L, R = [random.randint(0,6) for _ in range(4)]
    return [T, D, L, R]

def get_synthesizer(writer, checker, budget):
    def synthesizer(spec):
        prog = writer(spec)
        for i in range(budget):
            prog = writer(spec)
            if checker(prog, spec):
                return (i, prog)
        return None
    return synthesizer

synthesizer = get_synthesizer(random_writer, is_correct, 1000)
spec1 = [((0,4), outside), ((4,1), outside), ((1,1), inside), ((3,3), inside)]
res = synthesizer(spec1)
if res is not None:
    print(res)

# use grass coords to guess better
def better_writer(spec):
    inside_coords = [coord for coord,bool in spec if bool]
    if inside_coords == []:
        return random_writer(spec)
    row_coords = [coord[0] for coord in inside_coords]
    col_coords = [coord[1] for coord in inside_coords]
    T, D = random.choice(row_coords), random.choice(row_coords)
    L, R = random.choice(col_coords), random.choice(col_coords)
    return [T, D, L, R]

synthesizer2 = get_synthesizer(better_writer, is_correct, 1000)
res = synthesizer2(spec1)
if res is not None:
    print(res)