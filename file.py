from src.instruction_repository import InstructionRepostory

allOpCodes = map(lambda i: i.opcodes, InstructionRepostory._instructionSet)
flattened = []

for l in allOpCodes:
    for opcode in l:
        flattened.append(opcode)


# print(len(flattened))
# print(len(set(flattened)))
unique = list(set(flattened))
nonunique = []

def isunique(item):
    count = 0
    for i in flattened:
        if i == item:
            count += 1
    return count == 1

for item in flattened:
    if not isunique(item):
        nonunique.append(item)

nonunique = set(nonunique)
print(len(nonunique))
for i in nonunique:
    print((hex(i)))