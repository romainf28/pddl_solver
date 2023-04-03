from enum import Enum


class Operator(Enum):
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    IMP = "IMP"


class Node:

    def __init__(self, node_id, op=None, left=None, right=None, label=None):
        self.id = node_id
        self.op = op  # None if it is a variable
        self.left = left  # left operand
        self.right = right  # right operand
        self.label = label  # optional label
        self.reference_count = 0  # reference count for garbage collection
        if left is not None:
            left.reference_count += 1
        if right is not None:
            right.reference_count += 1

    def display(self, print_id=False, print_label=False):

        def get_id(i, flag):
            return ":" + str(i) if flag else ""

        if self.op is None:
            if print_label and self.label is not None:
                print(str(self.label), end=' ')
            else:
                print("v" + str(self.id), end=' ')
        else:
            print("(" + self.op.name + get_id(self.id, print_id), end=' ')
            if self.left is not None:
                self.left.display(print_id, print_label)
            print("", end=' ')
            if self.right is not None:
                self.right.display(print_id, print_label)
            print(")", end=' ')


class Formula:
    def __init__(self):
        self.last_id = 0
        self.reusable = list()  # When deleting a node, reuse the unique id
        self.node_to_id = dict()  # Get node id from node
        self.id_to_node = [None]  # Get node from node id
        self.name_to_id = dict()  # Get node id from label

    def get_id(self):
        '''
        Get a new id or reuse some
        '''
        if len(self.reusable) == 0:
            self.id_to_node.append(None)
            self.last_id += 1
            return self.last_id
        else:
            return self.reusable.pop()

    def create_var(self, name=None):
        '''
        Creates a new variable
        '''
        if name is not None:
            node_id = self.name_to_id.get(name)
            if node_id is not None:
                return self.id_to_node[node_id]
        node_id = self.get_id()
        node = Node(node_id, label=name)
        self.node_to_id[node] = node_id
        self.id_to_node[node_id] = node
        if name is not None:
            self.name_to_id[name] = node_id
        return node

    def create_var_array(self, litterals):
        assert (len(litterals) > 0)

        output_list = []
        for litt in litterals:

            if litt < 0:
                output_list.append(self.make_not(self.create_var(-litt)))
            else:
                output_list.append(self.create_var(litt))
        return output_list

    def make_operator(self, temp):
        node_id = self.node_to_id.get(temp)
        if node_id is not None:
            node = self.id_to_node[node_id]
            node.reference_count += 1
            return node
        else:
            # Create a new subformula node
            node_id = self.get_id()
            temp.id = node_id
            self.id_to_node[node_id] = temp
            self.node_to_id[temp] = node_id
        return temp

    def make_operator_from_array(self, litterals, op):
        assert (len(litterals) != 0)

        if len(litterals) == 1:
            return litterals[0]
        # Create a balanced tree
        left_half = self.make_operator_from_array(
            litterals[:len(litterals) // 2], op)
        right_half = self.make_operator_from_array(
            litterals[len(litterals) // 2:len(litterals)], op)
        temp = Node(0, op=op, left=left_half, right=right_half)
        return self.make_operator(temp)

    def make_not(self, left):
        temp = Node(0, op=Operator.NOT, left=left)
        return self.make_operator(temp)

    def make_and(self, left, right):
        temp = Node(0, op=Operator.AND, left=left, right=right)
        return self.make_operator(temp)

    def make_implication(self, left, right):
        temp = Node(0, op=Operator.IMP, left=left, right=right)
        return self.make_operator(temp)

    def make_and_from_array(self, litterals):
        return self.make_operator_from_array(litterals, op=Operator.AND)

    def make_or_from_array(self, litterals):
        return self.make_operator_from_array(litterals, op=Operator.OR)
