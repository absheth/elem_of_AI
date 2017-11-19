

# try:
#     states_file = open('moves1.txt', 'a')
# except IOError:
#     states_file = open('moves1.txt', 'w')
#
# states_file.write("Akash\n")


with open ("moves1.txt", "r") as myfile:
    for line in myfile:
        print line.strip()


# states_file.close()
