#!/bin/python3

import math
import os
import random
import re
import sys


class SinglyLinkedListNode:
	def __init__(self, node_data):
		self.data = node_data
		self.next = None



class SinglyLinkedList:
	def __init__(self):
		self.head = None
		self.tail = None

	def insert_node(self, node_data):
		node = SinglyLinkedListNode(node_data)

		if not self.head:
			self.head = node
		else:
			self.tail.next = node

		self.tail = node


def print_singly_linked_list(node, sep, fptr):
	while node:
		fptr.write(str(node.data))

		node = node.next

		if node:
			fptr.write(sep)



#
# Complete the 'deleteOdd' function below.
#
# The function is expected to return an INTEGER_SINGLY_LINKED_LIST_NODE.
# The function accepts INTEGER_SINGLY_LINKED_LIST_NODE listHead as parameter.
#

#
# For your reference:
#
# SinglyLinkedListNode:
#     int data
#     SinglyLinkedListNode next
#
#

def deleteOdd(listHead):
	count = 0
	while listHead and count < 10**5:
		if listHead.data % 2 == 0:
			try:
				del listHead.data
			except TypeError:
				continue
		listHead = listHead.next
	listHead



def print_singly_linked_list(node, sep=','):
    while node:
        print(str(node.data))

        node = node.next

        if node:
            print(sep)


if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

	listHead_count = 5

	listHead = SinglyLinkedList()

	for i in range(10):
		listHead.insert_node(i)



	print(deleteOdd(listHead.head))






	#print(listHead.head.__dict__['next'].__dict__['next'].__dict__)
	#print(listHead.head.__dict__['next'].__dict__['next'].__dict__['next'].__dict__)
from itertools import groupby

for i in groupby('12121211'))