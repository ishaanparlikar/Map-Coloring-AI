# Talha Muhammad, Said Siraj
# CS480 Fall 2017
# Dr.  Duric
# Project

import random   # Used to randomly choose a color for cutset
import copy     # Copy.deepcopy used to copy and preserve original objects in arrays


# A node be one state or "area" on a ma
class Node:
    def __init__(self, name, adjacent=None):
        self.name = name    # Nodes Name
        self.adjacent = adjacent    # Names of adjacent Nodes
        self.color_picked = None    # The assigned Color
        self.possible_colors = ["R", "B", "G", "Y"]  # The colors available to be used (4 colors)

    # A helper function that will remove a certain node from its adjacent list
    def remove_adjacent(self, node):
        if node in self.adjacent:
            self.adjacent.remove(node)

    # A helper function that will remove a certain color from the list of possible colors
    def remove_color(self, color_to_remove):
        if color_to_remove in self.possible_colors:
            self.possible_colors.remove(color_to_remove)

    # Returns the nodes degree by returning number of adjacent nodes
    def get_degree(self):
        return len(self.adjacent)

    # Assigns a color to the node and then finds the adjacent nodes in the graph passed in and removes the selected
    # color from those adjacent nodes
    def assign_color(self, color_to_assign, graph):
        self.color_picked = color_to_assign
        for node in self.adjacent:
            find_node(graph, node).remove_color(color_to_assign)

    # Resets node to uncolored with all colors available
    def reset(self):
        self.color_picked = None
        self.possible_colors = ["R", "B", "G", "Y"]

    # Returns true if color assigned. False otherwise
    def is_colored(self):
        if self.color_picked is None:
            return False
        else:
            return True

    # Elegant print out of the node. If color not assigned, Possible colors will be output as well
    # Useful for debugging
    def print(self):
        print()
        print("NODE " + self.name)
        print("=======")
        print("Adjacent " + str(self.adjacent))
        print("Color: " + str(self.color_picked))
        if self.color_picked is None:
            print("Possible Colors: " + str(self.possible_colors))

    # Helper function to check if a certain color is still available
    def is_color_avail(self, color_to_check):
        if color_to_check in self.possible_colors:
            return True
        else:
            return False


# Looks through the graph to see if ever node is colored and every node has a different color than its adjacent nodes
def validity_check(graph):
    for node in graph:
        current_color = node.color_picked
        if current_color is None:
            return False
        else:
            for comp_node in node.adjacent:
                if find_node(graph, comp_node).color_picked == current_color:
                    return False
    return True


# Searches through graph for the Node object who's name is = to name
def find_node(graph, name):
    for node in graph:
        if node.name == name:
            return node
    return None


# Gracefully removes a node from the graph. First, removes the node from the graph, Then removes node from any node's
# adjacency array
def remove_node_from_graph(graph, name):
    new_graph = copy.deepcopy(graph)
    removed_node = None
    for node in new_graph:
        if node.name == name:
            removed_node = node
            new_graph.remove(node)
            break
    for node in removed_node.adjacent:
        find_node(new_graph, node).remove_adjacent(name)
    return new_graph


# Utility function to reset every node in a graph
def reset_graph(graph):
    fresh_graph = copy.deepcopy(graph)
    for node in fresh_graph:
        node.reset()
    return fresh_graph


# Returns true if every node in graph is colored, else returns false
def is_graph_completely_colored(graph):
    for node in graph:
        if node.color_picked is None:
            return False
    return True


# This function colors the cutset and the remaining trees. See comments for the logic
def color(cutset, trees, og_graph):
    colored_graph = copy.deepcopy(og_graph)  # colored_graph is a deepcopy so we can preserve the og_graph
    verified = False    # This will become True once colored_graph is verified as a correct solution

    # We loop until we haven't verified. We can do this because the Four Color Theorem promises us a solution
    while not verified:
        # We start out by coloring each node in the cutset a random choice between the available colors for that
        # node. Whenever a node is colored all nodes adjacent to it lose that color as an available color.
        for node in cutset:
            node_in_graph = find_node(colored_graph, node)  # Finding the node in the graph
            node_in_graph.assign_color(random.choice(node_in_graph.possible_colors), colored_graph)  # Random color

        # We must finish coloring the rest of the graph. We will keep looping until the graph is not completely colored
        while not is_graph_completely_colored(colored_graph):
            # We will find the largest degree node to act as the trees root from the tree(s) available
            largest_degree_to_act_as_root = None
            fault = False   # fault will become true if we reach a point where a node cannot be colored

            # We find the largest degree node that is also not colored from trees
            for node in trees:
                if node.is_colored():
                    pass
                elif largest_degree_to_act_as_root is None and not node.is_colored():
                    largest_degree_to_act_as_root = node.name
                elif node.get_degree() > find_node(trees, largest_degree_to_act_as_root).get_degree() and \
                        not node.is_colored():
                    largest_degree_to_act_as_root = node.name

            # To keep colored graph and trees in sync. We color the node in both. Here we find the object node in both
            node_in_graph_colored = find_node(colored_graph, largest_degree_to_act_as_root)
            node_in_graph_tree = find_node(trees, largest_degree_to_act_as_root)

            # We attempt to color the graph with the least amount of colors. To do this, we try to color the node in
            # the following order - Red, Blue, Green, Yellow. Once we find which one is available, we assign the color.
            # NOTE, the is_color_avail must be done in colored_graph, as the available colors in the trees may be
            # different since they do not account for the cut
            if node_in_graph_colored.is_color_avail("R"):
                node_in_graph_colored.assign_color("R", colored_graph)
                node_in_graph_tree.assign_color("R", trees)
            elif node_in_graph_colored.is_color_avail("B"):
                node_in_graph_colored.assign_color("B", colored_graph)
                node_in_graph_tree.assign_color("B", trees)
            elif node_in_graph_colored.is_color_avail("G"):
                node_in_graph_colored.assign_color("G", colored_graph)
                node_in_graph_tree.assign_color("G", trees)
            elif node_in_graph_colored.is_color_avail("Y"):
                node_in_graph_colored.assign_color("Y", colored_graph)
                node_in_graph_tree.assign_color("Y", trees)

            # Now we attempt to color the adjacent nodes in the same way
            for node in node_in_graph_colored.adjacent:
                node_in_graph_2 = find_node(colored_graph, node)

                # At this stage, there may be a node who has no colors that it may be. In this case, we flag a fault
                if len(node_in_graph_2.possible_colors) == 0 and not node_in_graph_2.is_colored():
                    fault = True
                elif node_in_graph_2.is_color_avail("R") and not node_in_graph_2.is_colored():
                    node_in_graph_2.assign_color("R", colored_graph)
                elif node_in_graph_2.is_color_avail("B") and not node_in_graph_2.is_colored():
                    node_in_graph_2.assign_color("B", colored_graph)
                elif node_in_graph_2.is_color_avail("G") and not node_in_graph_2.is_colored():
                    node_in_graph_2.assign_color("G", colored_graph)
                elif node_in_graph_2.is_color_avail("Y") and not node_in_graph_2.is_colored():
                    node_in_graph_2.assign_color("Y", colored_graph)

            # If we hit a fault, we will break out of this loop and the validity check will fail and restart
            if fault:
                break

        # At this point, we cannot continue coloring with the current random coloring of the cutset. We check for
        # validity and if we are not valid, we will reset the colored graph and trees and let the loop start again
        verified = validity_check(colored_graph)
        if not verified:
            colored_graph = reset_graph(colored_graph)
            trees = reset_graph(trees)

    # If we are done with the loop, we ill return the graph
    return colored_graph


# Returns a small graph like the one in sample.png - Helpful for testing
def test_graph():
    graph = [Node("A", ["B", "C", "D"]),
             Node("B", ["A", "D"]),
             Node("C", ["A", "D"]),
             Node("D", ["A", "B", "C", "E"]),
             Node("E", ["D"]),
             Node("F")]
    return graph


# Returns the full USA graph. Each state is encapsulated in a node object.
def usa_graph():
    return [
            Node("AL", ["GA", "FL", "MS", "TN"]),
            Node("AK", []),
            Node("AZ", ["CA", "NV", "UT", "CO", "NM"]),
            Node("AR", ["TX", "OK", "MO", "TN", "MS", "LA"]),
            Node("CA", ["OR", "NV", "AZ"]),
            Node("CO", ["NM", "AZ", "UT", "WY", "NE", "KS", "OK"]),
            Node("CT", ["RI", "NY", "MA"]),
            Node("DE", ["MD", "PA", "NJ"]),
            Node("DC", ["MD", "VA"]),
            Node("FL", ["GA", "AL"]),
            Node("GA", ["SC", "NC", "TN", "AL", "FL"]),
            Node("HI", []),
            Node("ID", ["WA", "OR", "NV", "UT", "WY", "MT"]),
            Node("IL", ["WI", "IA", "MO", "KY", "IN"]),
            Node("IN", ["IL", "KY", "OH", "MI"]),
            Node("IA", ["MN", "SD", "NE", "MO", "IL", "WI"]),
            Node("KS", ["CO", "OK", "MO", "NE"]),
            Node("KY", ["MO", "TN", "VA", "WV", "OH", "IN", "IL"]),
            Node("LA", ["TX", "AR", "MS"]),
            Node("ME", ["NH"]),
            Node("MD", ["DE", "PA", "WV", "DC", "VA"]),
            Node("MA", ["RI", "CT", "NY", "VT", "NH"]),
            Node("MI", ["OH", "IN", "WI"]),
            Node("MN", ["WI", "IA", "SD", "ND"]),
            Node("MS", ["LA", "AR", "TN", "AL"]),
            Node("MO", ["KS", "NE", "IA", "IL", "KY", "TN", "AR", "OK"]),
            Node("MT", ["ID", "WY", "SD", "ND"]),
            Node("NE", ["WY", "SD", "IA", "MO", "KS", "CO"]),
            Node("NV", ["CA", "OR", "ID", "UT", "AZ"]),
            Node("NH", ["ME", "MA", "VT"]),
            Node("NJ", ["NY", "PA", "DE"]),
            Node("NM", ["AZ", "UT", "CO", "OK", "TX"]),
            Node("NY", ["PA", "NJ", "CT", "MA", "VT"]),
            Node("NC", ["VA", "TN", "GA", "SC"]),
            Node("ND", ["MT", "SD", "MN"]),
            Node("OH", ["PA", "WV", "KY", "IN", "MI"]),
            Node("OK", ["TX", "NM", "CO", "KS", "MO", "AR"]),
            Node("OR", ["WA", "ID", "NV", "CA"]),
            Node("PA", ["NY", "NJ", "DE", "MD", "WV", "OH"]),
            Node("RI", ["CT", "MA"]),
            Node("SC", ["GA", "NC"]),
            Node("SD", ["WY", "MT", "ND", "MN", "IA", "NE"]),
            Node("TN", ["AR", "MO", "KY", "VA", "NC", "GA", "AL", "MS"]),
            Node("TX", ["NM", "OK", "AR", "LA"]),
            Node("UT", ["CO", "NM", "AZ", "NV", "ID", "WY"]),
            Node("VT", ["NY", "MA", "NH"]),
            Node("VA", ["NC", "TN", "KY", "WV", "MD", "DC"]),
            Node("WA", ["ID", "OR"]),
            Node("WV", ["KY", "OH", "PA", "MD", "VA"]),
            Node("WI", ["MN", "IA", "IL", "MI"]),
            Node("WY", ["ID", "MT", "SD", "NE", "CO", "UT"])
        ]


# Runs the cutset algorithm and returns the cutset
def remove_cutset(graph):
    cutset = []  # Will hold the cutset nodes
    rest = copy.deepcopy(graph)  # Deep copy of graph to preserve graph

    # We will loop through and remove any nodes from graph who's degree is 1 and 0
    while True:
        graph_changed = False  # If Graph changes we turn this flag on to indicate there may be more nodes to remove
        for node in rest:
            if node.get_degree() <= 1:
                rest.remove(node)
                graph_changed = True
                for adjacent_node in node.adjacent:
                    find_node(rest, adjacent_node).remove_adjacent(node.name)
        if not graph_changed:
            # If graph did not change this loop, we are done
            break

    # Now we will begin to remove the cutset nodes
    while True:
        # If the graph is empty we are done and we should break
        if len(rest) == 0:
            break
        # We need to find the ndoe with the biggest degree, We will loop through rest to find it
        largest_deg_node = None
        for node in rest:
            if largest_deg_node is None:
                largest_deg_node = node
            elif node.get_degree() > largest_deg_node.get_degree():
                largest_deg_node = node
        # We will remove it from rest and add the name of the node into cutset
        rest.remove(largest_deg_node)
        cutset.append(largest_deg_node.name)

        # We will remove this node from its adjacent nodes adjacency list
        for adjacent_node in largest_deg_node.adjacent:
            find_node(rest, adjacent_node).remove_adjacent(largest_deg_node.name)

        # We will once again remove all nodes with degree 0 or 1 the same way
        while True:
            graph_changed = False
            for node in rest:
                if node.get_degree() <= 1:
                    rest.remove(node)
                    graph_changed = True
                    for adjacent_node in node.adjacent:
                        find_node(rest, adjacent_node).remove_adjacent(node.name)
            if not graph_changed:
                break
    # We now have out cutset
    return cutset


# Main function. Runs coloring on the USA map
def main():
    # Initialize graph
    graph = usa_graph()

    # Extract the cutset
    cutset = remove_cutset(graph)

    # Trees will hold the original graph with the cutset removed
    trees = copy.deepcopy(graph)

    # Remove cutset from tree
    for node in cutset:
        trees = remove_node_from_graph(trees, node)

    # Color the graph
    colored = color(cutset, trees, graph)

    # Print out graph elegantly
    for node in colored:
        node.print()

    # Run verification one last time :)
    print("\nVerified: " + str(validity_check(colored)))


if __name__ == "__main__":
    main()

# Talha Muhammad & Saif Siraj
