# -*- coding: utf-8 -*-

#Please note: This program is written in Python2.

#Named Entity Recognition: dictionary lookup approach
#considering capitalization and suffixes 
#by Miriam Kümmel

#This program exemplarily shows a dictionary lookup
#approach to Named Entity Recognition.

#Orange headings help in orientation.

"""Preparations for the program"""
import string
import re
from sets import Set

inputText = open("hp1.txt", "r") #input text
lines = list(inputText) #reads in text linewise

#***exemplary*** dictionaries for NEs, suffixes and words to exlcude:
dictionaryPerson = ["Hermione", "Ron", "Dursley", "Harry Potter", "Rowling", 
					"Harvey", "Harry's", "Voldemort", "Albus Dumbledore", 
					"Mr", "Mrs", "Jim", "Harold", "Dudley", "Grunnings"]
dictPerComp = string.join(dictionaryPerson)
dictPerComp2 = string.split(dictPerComp) #dictionary with single words

dictionaryLocation = ["Scotland", "West Country", "Devon", "Dundee", "Surrey", "England", "Hogwarts", 
						"Britain", "Kent", "Privet Drive", "Yorkshire"]
dictLocComp = string.join(dictionaryLocation)
dictLocComp2 = string.split(dictLocComp) #dictionary with single words

dictionaryOrganization = ["Hogwarts School of Witchcraft and Wizardry"]
dictOrgComp = string.join(dictionaryOrganization)
dictOrgComp2 = string.split(dictOrgComp) #dictionary with single words

toExclude = ["English", "British", "I", "Tuesday"]
suffixPersons = ["ia", "ez", "son"]

#lists for recognized and classified NEs
foundEntitiesPerson = []
foundEntitiesLocation = []
foundEntitiesOrganizations = []

cap = re.compile(r"\w\s[A-Z][A-Za-z]*[\-]*[A-Za-z]*[\-]*[A-Za-z]*") #Regular Expression

#lists for unknown NEs
listOfCaps = []
listOfCaps2 = []
listOfCaps3 = []
listOfCaps4 = []
listOfCaps5 = []
listOfCaps6 = []
listOfCaps7 = []

"""List Lookups"""		
for line in lines: #iterates the input document linewise
	for entry in dictionaryPerson: #iterates the dictionary of person NEs
		if entry in line and entry not in foundEntitiesPerson: #compares word to entry; only append once
			foundEntitiesPerson.append(entry)

	for entry2 in dictionaryLocation:
		if entry2 in line and entry2 not in foundEntitiesLocation and entry2 not in foundEntitiesPerson: #person-NEs are privileged
			foundEntitiesLocation.append(entry2)
			
	for entry3 in dictionaryOrganization:
		if entry3 in line and entry3 not in foundEntitiesOrganizations and entry3 not in foundEntitiesPerson:
			foundEntitiesOrganizations.append(entry3)
print "\nDONE!"		
print "\nThe following Location-NEs have been found:\n", foundEntitiesLocation, "Total:", len(foundEntitiesLocation)
print "The following Organization-NEs have been found:\n", foundEntitiesOrganizations, "Total:", len(foundEntitiesOrganizations)
print "The following Person-NEs have been found:\n", foundEntitiesPerson, "Total:", len(foundEntitiesPerson), "\n"


"""Using RE for spotting capitalization"""
print "\nUknown NEs\nThese are the capitalized words that are not at the beginning of a sentence and not an exception:"
for line in lines: #iterates linewise
	capsis = cap.findall(line) #applies RE on document
	listOfCaps.append(capsis)
	listOfCaps2 = [x for y in listOfCaps for x in y] #list comprehension
	listOfCaps3 = set(listOfCaps2) #transform to set to exclude duplicates
	listOfCaps4 = list(listOfCaps3) #back to list
	
for i in listOfCaps4:
	capsEx = i[2:] #remove first two characters (\w\s)
	if capsEx not in dictionaryPerson and capsEx not in dictionaryOrganization and capsEx not in dictionaryLocation and capsEx not in toExclude and capsEx not in dictLocComp2 and capsEx not in dictPerComp2:
		listOfCaps5.append(capsEx) #only append if not known before
	listOfCaps6 = set(listOfCaps5) #transform to set to exclude duplicates
	listOfCaps7 = list(listOfCaps6) # transform back to list
	
#ignore plural-s and other derivation/inflection
for v in listOfCaps7: #iterates unknown NEs
	for o in dictLocComp2: #iterates split up dictionary
		if o in v or v in o: #if word out of split up dict is in NE or vice versa
			listOfCaps7.remove(v) #remove from list of NEs
for q in listOfCaps7:
	for g in dictPerComp2:
		if g in q or q in g:
			listOfCaps7.remove(q)
for w in listOfCaps7:
	for n in dictOrgComp2:
		if n in w or w in n:
			listOfCaps7.remove(w)

print listOfCaps7, "\nTotal number unkown NEs:", len(listOfCaps7)

"""Exemplary suffix-research"""
for x in listOfCaps7: #iterates unkown NEs
	for y in suffixPersons: #iterates suffixes
		if y in x: #if suffix in NE
			foundEntitiesPerson.append(x)
			print "\nA new NE has been added to Person-NEs due to its suffix!:\n", x 
			print "\nHere are the found person-entities again:\n", foundEntitiesPerson, "\nTotal now:", len(foundEntitiesPerson)
