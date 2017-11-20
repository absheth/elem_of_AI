#   Akash Sheth, 2017 || Game of Chance
#   Ref[1]: https://stackoverflow.com/questions/2213923/python-removing-duplicates-from-a-list-of-lists
#   Ref[2]: https://stackoverflow.com/questions/10272898/multiple-if-conditions-in-a-python-list-comprehension
#   Ref[3]: https://stackoverflow.com/questions/25010167/e731-do-not-assign-a-lambda-expression-use-a-def
import itertools

# take the input from user
print "Enter the space separated roll configuration: "
roll_config = map(int, raw_input().split())


# calculate the score
def calculate_score(roll):
    return 25 if roll[0] == roll[1] and roll[1] == roll[2] else sum(roll)


# returns the configuration with expected score
def max_node(roll, configuration):
    # lambda -- Ref[2], Ref[3]
    def a(roll_a): return roll_a[0] if roll_a[1] else roll_a[2]
    # lambda -- Ref[2], Ref[3]

    all_combinations = [[a([roll_a, configuration[0], roll[0]]),
                         a([roll_b, configuration[1], roll[1]]),
                         a([roll_c, configuration[2], roll[2]])] for roll_a in range(1, 7) for roll_b in range(1, 7) for roll_c in range(1, 7)]
    # remove all the duplicates
    # Ref[1] -- START
    all_combinations.sort()
    no_dup_combos = list(all_combinations for all_combinations, _ in itertools.groupby(all_combinations))
    # Ref[1] -- END
    return [configuration, sum(calculate_score(rolls) for rolls in no_dup_combos) / float(len(no_dup_combos))]


# Finds the next roll
def find_next_roll(roll_config):

    whether_roll = [True, False]
    current_max = [0, 0]
    for dice_1 in whether_roll:
        for dice_2 in whether_roll:
            for dice_3 in whether_roll:
                new_max = max_node(roll_config, [dice_1, dice_2, dice_3])
                current_max = new_max if new_max[1] > current_max[1] else current_max
    return current_max


solution = find_next_roll(roll_config)
print "Next roll -->", solution[0], "|| Expected Score -->", solution[1]
