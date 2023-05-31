"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMayInLeftSubtreeTonode(node):
            # Replace node's datum with the mayimum datum in the left subtree
            # Pre:  node has a left child
            # Post: the mayimum node in node's left subtree
            #       has been removed
            # Post: node.data = mayimum value in node's left subtree
            parent = node
            currentNode = node.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            node.data = currentNode.data
            if parent == node:
                node.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the mayimum value in the
        #         left subtree
        #         Delete the mayimium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMayInLeftSubtreeTonode(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        if self._root is None:
            return -1
        def height1(node):
            '''
            Helper function
            :param node:
            :return:
            '''
            if node.left is None or node.right is None:
                return 0
            else:
                return 1 + max(height1(node.left), height1(node.right))
        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return True if self.height() <= 2 * log(self._size + 1, 2) - 1 else False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        return [elem for elem in self.inorder() if low <= elem <= high]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        lyst = []
        for elem in self.inorder():
            lyst.append(elem)

        self.clear()
        tree = self.build_balanced_tree(lyst)
        self._root = tree._root
        self._size = tree._size

    def build_balanced_tree(self, lyst):
        '''
        Builds a balanced tree from a sorted list.
        :param lyst:
        :return:
        '''
        tree = LinkedBST()
        tree._root = self.build_balanced_tree_helper(lyst)
        tree._size = len(lyst)
        return tree

    def build_balanced_tree_helper(self, lyst):
        '''
        Helper function for build_balanced_tree
        :param lyst:
        :return:
        '''
        if not lyst:
            return None
        mid = len(lyst) // 2
        root = BSTNode(lyst[mid])
        root.left = self.build_balanced_tree_helper(lyst[:mid])
        root.right = self.build_balanced_tree_helper(lyst[mid + 1:])
        return root

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lyst = [e for e in self.inorder()]
        for el in self.inorder():
            if el == min(lyst) and el > item:
                return el
            else:
                lyst.remove(el)
        return item

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lyst = [e for e in self.inorder()]
        for el in self.inorder():
            if el == max(lyst) and el < item:
                return el
            else:
                lyst.remove(el)
        return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        import matplotlib.pyplot as plt
        import random
        import numpy as np
        import timeit
        import sys
        sys.setrecursionlimit(250000)
        with open(path, 'r', encoding = 'utf-8') as words: lyst = words.read().split('\n')
        lyst_1 = lyst
        tree = LinkedBST()
        tree_shuffled = LinkedBST()
        tree_rebalanced = LinkedBST()
        for el in lyst:
            tree.add(el)
        for el__ in lyst:
            tree_rebalanced.add(el__)
        tree_rebalanced.rebalance()
        random.shuffle(lyst)
        for el_ in lyst:
            tree_shuffled.add(el_)

        # y_1 = lyst
        # y_2 = [el for el in tree.inorder()]
        # y_3 = [el for el in tree_shuffled.inorder()]
        # y_4 = [el for el in tree_rebalanced.inorder()]
        # y = [y_1, y_2, y_3, y_4]

        word = 'abnet'
        x_1 = timeit.timeit(lambda: lyst.index(word))
        x_2  = timeit.timeit(lambda: tree.find(word))
        x_3  = timeit.timeit(lambda: tree_shuffled.find(word))
        x_4  = timeit.timeit(lambda: tree_rebalanced.find(word))

        x = [x_1, x_2, x_3, x_4]
        z = ['list', 'tree', 'tree_shuffled', 'tree_rebalanced']
        plt.bar(z, x)
        plt.show()

b = LinkedBST()
b.demo_bst('words.txt')

