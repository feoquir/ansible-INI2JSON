#!/usr/bin/env python
#
#	Ansible inventory converter: from INI to JSON
#

import re, json

__author__= 'FeoQuir'

def ini2json(file_string):
	#print("Original file:\n##########################\n"+file_string+"##########################\n")
	# Defining master dictionary
	json_inventory={"_meta":{"hostvars":{}}}
	# Reading text line by line
	for line in file_string.split("\n"):
		# Defining if the line is a group
		if re.match(r'^\[.*\]$',line.strip()):
			# Stripping and splitting group value
			grp=line.strip('[').strip(']').split(':')
			# Defining group value. if blank, use default hosts
			try:
				grp_type = grp[1]
			except:
				grp_type = 'hosts'
			# Based on the type of group, creating either a blank dictionary or string
			if grp_type == 'vars': subgrp = {grp_type:{}}
			else: subgrp = {grp_type:[]}
			# If the group was defined before, update it with the new group type
			if grp[0] in json_inventory:
				json_inventory[grp[0]].update(subgrp)
			# If the group was not defined, update master dictionary
			else:
				json_inventory.update({grp[0]:subgrp})
		# Defining group members
		elif line.strip():
			# Commented values verification
			if not re.match(r'^\#.*',line):
				# Checking if the subgroup was defined as a var
				if grp_type == 'vars':
					# Defining variable values, while clearing all blank spaces
					grp_var = line.replace(' ','').split('=')
					# Updating dictionary with the var values
					json_inventory[grp[0]][grp_type].update({grp_var[0]:grp_var[1]})
				else:
					# Curating host value and possible variable list
					member=line.strip().replace('=',' ').split()
					# Updating dicitonary with children/hosts
					json_inventory[grp[0]][grp_type].append(member[0])
					# Verifying if there are variables
					if len(member) != 1:
						# Blank dictionary for host variables
						membvar={member[0]:{}}
						# Filling host variables dictionary
						for i in range(1,len(member),2):
							membvar[member[0]].update({member[i]:member[i+1]})
						# Updating hostvars dictionary
						json_inventory['_meta']['hostvars'].update(membvar)
	# JSON return
	return json.dumps(json_inventory, indent=1, sort_keys=True)