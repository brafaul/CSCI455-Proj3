testFile = open("tests.txt", "w")
for i in range(0, 8281, 10):
    testFile.write("D" + str(i) + '\n')
