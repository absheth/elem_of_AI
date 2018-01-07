#!/usr/bin/env python
# 	Akash Sheth, 2017 (bmallala-absheth-pjuneja-a1)
#
#	Collaborated with aarigela-shahrama-cpatil-a1 to discuss the approach.
#	
#	We have used Local Search for the implementation of this program.
#	
#	Initial state: All the students will be considered as one group i.e. No of groups = No of students.
#	Successor state: Combination of each student with another student will be the successor state.
#	For ex:
#
#	Input file-
#		
#		djcran 3 zehzhang,chen464 kapadia
#		chen464 1 _ _
#		fan6 0 chen464 djcran
#		zehzhang 1 _ kapadia
#		kapadia 3 zehzhang,fan6 djcran
#		steflee 0 _ _problem2
#	
#	Initial state: (djcran),(chen464),(fan6),(zehzhang),(kapadia),(steflee)
#
#	Successor states: 
#		(djcran, chen464),(fan6),(zehzhang),(kapadia),(steflee)
#		(djcran, fan6),(chen464),(zehzhang),(kapadia),(steflee)
#		(djcran, zehzhang),(chen464),(fan6),(kapadia),(steflee)
#		.
#		.
#		.
#		.
#		.
#		(djcran),(chen464),(fan6),(kapadia),(zehzhang, steflee)
#		(djcran),(chen464),(fan6),(zehzhang),(kapadia, steflee)
#		
#		
#		
#	Cost function: Total time = (k*no_of_teams) + l + (n*no_students_not_assigned_as_positive_pref) + (m*no_students_assigned_as_negative_pref)
#	
#	where, 	k --> Time for grading 1 group
#			l --> No of students who do not get their size preference
#			m --> Time for meeting with each student who are assigned to someone they do no want to work with
#			n --> Time for the instructor to read and respond to the complaint email
#	
#	Goal state: Combination of groups that takes the lowes time for the faculty (cost).
#			

import sys
import copy
from Queue import PriorityQueue

file_name 	=	sys.argv[1]
global_k	=	int(sys.argv[2])
global_m	=	int(sys.argv[3])
global_n	=	int(sys.argv[4])



#Opening the file and reading the data from it
#Reference:- https://stackoverflow.com/questions/3277503/how-do-i-read-a-file-line-by-line-into-a-list
with open(file_name) as f:
    file_line_list 	= [[value for value in line.split()] for line in f]
#Reference:- https://stackoverflow.com/questions/3277503/how-do-i-read-a-file-line-by-line-into-a-list

#All the usernames
user_names			= [line[0] for line in file_line_list]

#Group size preferences of all the usernames
user_group_size_pref 	= {line[0]: line[1] for line in file_line_list}

#Group member preferenes of all the usernames
user_positive_pref 	= {line[0]: line[2] for line in file_line_list}
user_negative_pref 	= {line[0]: line[3] for line in file_line_list}


#This method checks whether elements in the second list exists in the first list
def if_exists_in_list(list_1, list_2):

	list_1_elements  = []
	list_2_elements  = []
	count	=	0
	if type(list_1) is not list:
		list_1_elements	=	[list_1]
	else:
		list_1_elements   = 	list_1

	if type(list_2) is not list:
		list_2_elements	=	[list_2]
	else:
		list_2_elements   = 	list_2

	"""for a in range(0,len(list_1_elements)):
					for b in range(0,len(list_2_elements)):
						if list_1_elements[a] == list_2_elements[b]:
							count = count + 1
			
				if count == len(list_2_elements):
					return True"""
	
	return set(list_2_elements) < set(list_1_elements)

#This function calculates cost of each of the state.
def calculate_cost(current_formation):
	count_for_group_size_conflict = 0
	count_for_m = 0
	count_for_n	= 0
	
	total_groups	=	len(current_formation)
	
	for each_group in current_formation:
		
		for each_member in each_group:
			
			if int(user_group_size_pref[each_member]) != len(each_group) and int(user_group_size_pref[each_member]) != 0:
				count_for_group_size_conflict = count_for_group_size_conflict + 1
			
			user_member_positive_preferences = user_positive_pref[each_member].split(',')
			
			for pref_member in user_member_positive_preferences:
				if pref_member != '_' and pref_member not in each_group:
					count_for_n = count_for_n + 1
			
			
			user_member_negative_preferences = user_negative_pref[each_member].split(',')
			for pref_member in user_member_negative_preferences:
				if pref_member != '_' and pref_member in each_group:
					count_for_m = count_for_m + 1

	total_cost = global_k*total_groups + count_for_group_size_conflict + global_n*count_for_n + global_m*count_for_m
	
	return total_cost

#This function generates successor of the current_team.
def new_teams(current_team):
	formation	=	[]
	form_team = []
	final_new_teams	=	[]
	list_created	=	False
	
	for i in range(0,len(current_team)):
		for j in range(i,len(current_team)):
			if j!=i:
				a = current_team[i]+current_team[j]
				if len(a) <= 3:
					form_team.append(a)

	for m in range(0,len(form_team)):
		append_cheker = False
		for k in range(0,len(current_team)):
			if not if_exists_in_list(form_team[m], current_team[k]):
				if not append_cheker:
					formation	=	copy.deepcopy([form_team[m]])
					formation.append(current_team[k])
					append_cheker = True
				else:
					formation.append(current_team[k])

		final_new_teams.append(formation)
		formation	=	[]
	
	if len(final_new_teams) == 0:
		final_new_teams.append(current_team)
	
	return [final_new_teams]

#This function gets the group combination with the lowest cost.
def get_groups_combo_with_lowest_cost(set_of_new_teams):
	#count_combo = []
	queue_for_cost_combos = PriorityQueue()
	cost_group_combo = []
	if len (set_of_new_teams) == 1:
		#return set_of_new_teams
		team = set_of_new_teams[0]
		cost_group_combo.append(calculate_cost(team))
		cost_group_combo.append(team)
		return cost_group_combo	
	
	for team_combination in set_of_new_teams:
		new_cost = calculate_cost(team_combination)
		#count_combo.append(new_cost)
		queue_for_cost_combos.put([new_cost, team_combination])
	
	#print count_combo
	a = queue_for_cost_combos.get()
	cost_group_combo.append(a[0])
	cost_group_combo.append(a[1])
	
	return cost_group_combo

#This function prints the solution.
def printable_solution(set_of_teams):
	print "\n".join([ " ".join([ col for col in row ]) for row in set_of_teams[1]])
	print set_of_teams[0]

#This function finds all the team formation that would minimize course staff's work.
def find_teams(initial_teams):
	
	group_list	=	[initial_teams]
	old_cost	=	calculate_cost(initial_teams)
	new_low_cost=	0
	final_groups	=	[]

	while len(group_list) > 0:
		popped_state = group_list.pop()
		for teams in new_teams( popped_state ):
			current_lowest_cost_team = get_groups_combo_with_lowest_cost(teams)
			new_low_cost = current_lowest_cost_team[0]
			if new_low_cost < old_cost:
				old_cost	=	new_low_cost
				group_list	=	copy.deepcopy([current_lowest_cost_team[1]])
			else:
				break
	return current_lowest_cost_team    


#Initial state
initial_teams	=	[[name] for name in user_names]	

#Find the solution
solution = find_teams(initial_teams)

#Printing the solution
printable_solution(solution)
