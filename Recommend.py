#
#   ----- C1623580 -----
#

import numpy as np
import math
from decimal import *

# Read text and return list of strings of each row
def readTxt (fileInput):
    with open(fileInput, 'r') as f:
        return ([l.rstrip() for l in f])

# Print list as if it was txt again
def returnTxt(listInput):
    for i in listInput:
        print(i)

# We use .count to count the number of times an entry occurs in the list we input.
# We are returned a dict with the entry, and number of times it's in the original list.
# If the number of times isn't 0, it is not a positive entry.
def positiveEntries(listInput):
    entries = 0
    for i in [[item,listInput.count(item)] for item in set(listInput[1:])]:
        entries += 1
    return entries

# Take a list, a row, and a column from row. Return a very specific single value from list.
def returnValueFromRow(listInput, rowNumber, columnNumber):
    return str(listInput[rowNumber]).split(" ")[columnNumber]

# Create a history for a specific customer of their unique purchases
def createCustomerPurchaseHistory(listInput, customerID, forItems = False):
    customerHistory = []
    if not forItems:
        for i in listInput[1:]:
            i = i.split(" ")
            if i[0] == str(customerID) and i[1] not in customerHistory:
                customerHistory.append(i[1])
    else:
        for i in listInput[1:]:
            i = i.split(" ")
            if i[1] == str(customerID) and i[0] not in customerHistory:
                customerHistory.append(i[0])
    return customerHistory

# Creates an empty dict to start. Then goes through the list of purchases,
# creating a new key if the customer ID is not in the dict. We then run the
# function to generate purchase history with the key, to make a dict of all
# customers' histories.
def createAllHistories(listInput, forItems = False):
    allHistories = {}
    if not forItems:
        for i in listInput[1:]:
            i = i.split(" ")
            if i[0] not in allHistories:
                customerHistory = createCustomerPurchaseHistory(listInput, i[0])
                allHistories[i[0]] = customerHistory
    else:
        for i in listInput[1:]:
            i = i.split(" ")
            if i[1] not in allHistories:
                customerHistory = createCustomerPurchaseHistory(listInput, i[1], forItems = True)
                allHistories[i[1]] = customerHistory
    return allHistories

# Take a customer's purchase history, and the number of itemsBought
# We then make a list with 1 if they purchased, 0 if they didn't
def customerItemPurchaseHistory(purchaseHistory, listInput, rowNumber, columnNumber):
    # We get the number of items from the returnValueFromRow function
    numberOfItems = returnValueFromRow(listInput, rowNumber, columnNumber)
    itemsBought = []
    for i in range(int(numberOfItems)):
        if str(i + 1) in purchaseHistory:
            itemsBought.append(1)
        else:
            itemsBought.append(0)
    return(itemsBought)

# Find the customer item purchase history for all customers and make it
# into a dict
def allCustomerItemPurchaseHistory(dictInput, listInput, forItems = False):
    allHistories = {}
    if not forItems:
        for key, item in dictInput.items():
            customerItems = customerItemPurchaseHistory(item, listInput, 0, 2)
            allHistories[key] = customerItems
    else:
        for key, item in dictInput.items():
            customerItems = customerItemPurchaseHistory(item, listInput, 0, 0)
            allHistories[key] = customerItems
    return allHistories

# Get a dict of items, and the customers who bought them. We basically have to
# reverse our functions. Comments will detail inside the function how we use them
def makeItemToItemDict(listInput):
    # We specify forItems = True, which runs the functions in a different manner
    # to create item-to-customer history

    allHistories = createAllHistories(listInput, forItems = True)
    itemHistoryDict = allCustomerItemPurchaseHistory(allHistories, listInput, forItems = True)
    return itemHistoryDict

# Calculate angle between 2 arrays
def calcAngle(array1, array2):
    #Convert arrays to numpy arrays to perform vector operations
    array1 = np.array(array1)
    array2 = np.array(array2)
    # Calculate angle using formula like in lecture notes
    norm1 = np.linalg.norm(array1)
    norm2 = np.linalg.norm(array2)
    cosTheta = np.dot(array1, array2) / (norm1 * norm2)
    theta = math.degrees(math.acos(cosTheta))
    return "%.2f" % theta

# Take a dict input of all the vectors. We then calculate all the angle pairs
# From the items in the dict, create a dict of the angles, and add it to a dict.
# A dict of dicts :-)
def calcAllAngles(dictInput):
    allAngles = {}
    for key, item in dictInput.items():
        keyAngles = {}
        for subkey, subitem in dictInput.items():
            if not key == subkey:
                angle = calcAngle(item, subitem)
                keyAngles[subkey] = angle
        allAngles[key] = keyAngles
    return allAngles

# We take our calculated dict of angles, then for each item make a list
# of floated copies of the strings. We use this to sort our angles, to Find
# the lowest for matching. If we have an angle < 90, that's our match, so
# we return the item ID and the angle. Otherwise, no match.


def matchItem(itemDict, queries, cart):
    for i in queries:
        anglesList = []
        itemToMatch = itemDict.get(i)
        for subkey, subitem in itemToMatch.items():
            if subkey not in cart:
                anglesList.append(float(subitem))
        sortedAngles = sorted(anglesList)
        if sortedAngles[0] < 90:
            for subkey, subitem in itemToMatch.items():
                if sortedAngles[0] == float(subitem):
                    return [subkey, sortedAngles[0]]
        else:
            return 'no match'

# Get an average for each angle calculation per item, add to a list
# then average this list to get total average.
def averageAngle(dictInput):
    allAngles = []
    for key, item in dictInput.items():
        angles = []
        for subkey, subitem in item.items():
            angles.append(float(subitem))
        allAngles.append(sum(angles) / len(angles))
    return "{:.2f}".format((sum(allAngles) / len(allAngles)))

# Convert a string to a list seperated at whitespace
def stringsToLists(listInput):
    stringList = []
    for i in listInput:
        if i != " ":
            stringList.append(i.split(" "))
    return stringList

def recommendOrder(matchesDict):
    itemsList = []
    for key, item in matchesDict.items():
        if type(item) == list and not any(item[0] == i[0] for i in itemsList):
                itemsList.append(item)
    # Lambda function to sort list of lists depending on angle in sublist
    itemsList.sort(key=lambda x: x[1])
    return itemsList


def recommend(itemHistory, queries):
    # Read in the txts
    itemHistory = readTxt(itemHistory)
    queries = readTxt(queries)
    # Turn our queries into lists
    queriesList = stringsToLists(queries)
    # Get our item-to-item history dict
    items = makeItemToItemDict(itemHistory)

    anglesDict = calcAllAngles(items)
    # Run the function to get the item-to-item angle matches
    # Format everything
    print("Positive entries: " + str(positiveEntries(itemHistory)))
    print("Average angle: " + averageAngle(anglesDict))
    # This row count is helpful for formatting, can iterate through non-list queries
    rowCount = 0

    for item in queriesList:
        # Make empty dict
        itemMatches = {}
        # Print cart from queries
        print("Shopping cart: " + str(queries[rowCount]))
        # For each item in our query
        for i in item:
            # Find a match for the item
            itemMatch = matchItem(anglesDict, i, item)
            itemMatches[i] = itemMatch
            # If the item is a list we know it's matched so print the item and the angle
            if type(itemMatch) == list:
                print("Item: " + i + "; match: " + itemMatch[0] + "; angle: " + str('{:.2f}'.format(itemMatch[1])))
            # Otherwise no matched
            else:
                print("Item: " + i + " no match")
        # Put our matches into a function that orders them based on best recommendation
        recommendOrderedList = recommendOrder(itemMatches)
        recommendString = ''
        for i in recommendOrderedList:
            recommendString += (" " + i[0])
        print("Recommend:" + recommendString)
        rowCount += 1

recommend('history2.txt', 'queries2.txt')
