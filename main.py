import random
import copy


class Node:
    def __init__(self, name, adjacent=None):
        self.name = name
        self.adjacent = adjacent
        self.color_picked = None
        self.possible_colors = ["R", "B", "G", "Y"]

    def remove_adjacent(self, node):
        if node in self.adjacent:
            self.adjacent.remove(node)

    def remove_color(self, color_to_remove):
        if color_to_remove in self.possible_colors:
            self.possible_colors.remove(color_to_remove)

    def get_degree(self):
        return len(self.adjacent)

    def assign_color(self, color_to_assign, graph):
        self.color_picked = color_to_assign
        for node in self.adjacent:
            find_node(graph, node).remove_color(color_to_assign)

    def reset(self):
        self.color_picked = None
        self.possible_colors = ["R", "B", "G", "Y"]

    def is_colored(self):
        if self.color_picked is None:
            return False
        else:
            return True

    def print(self):
        print()
        print("NODE " + self.name)
        print("=======")
        print("Adjacent " + str(self.adjacent))
        print("Color: " + str(self.color_picked))
        if self.color_picked is None:
            print("Possible Colors: " + str(self.possible_colors))

    def is_color_avail(self, color_to_check):
        if color_to_check in self.possible_colors:
            return True
        else:
            return False


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


def find_node(graph, name):
    for node in graph:
        if node.name == name:
            return node
    return None


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


def reset_graph(graph):
    fresh_graph = copy.deepcopy(graph)
    for node in fresh_graph:
        node.reset()
    return fresh_graph


def is_graph_completely_colored(graph):
    for node in graph:
        if node.color_picked is None:
            return False
    return True


def color(cutset, trees, og_graph):
    colored_graph = copy.deepcopy(og_graph)
    verified = False
    while not verified:
        for node in cutset:
            node_in_graph = find_node(colored_graph, node)
            node_in_graph.assign_color(random.choice(node_in_graph.possible_colors), colored_graph)

        while not is_graph_completely_colored(colored_graph):
            largest_degree_to_act_as_root = None
            fault = False
            for node in trees:
                if node.is_colored():
                    pass
                elif largest_degree_to_act_as_root is None and not node.is_colored():
                    largest_degree_to_act_as_root = node.name
                elif node.get_degree() > find_node(trees, largest_degree_to_act_as_root).get_degree() and \
                        not node.is_colored():
                    largest_degree_to_act_as_root = node.name
            # input("w3")

            node_in_graph_colored = find_node(colored_graph, largest_degree_to_act_as_root)
            node_in_graph_tree = find_node(trees, largest_degree_to_act_as_root)
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

            for node in node_in_graph_colored.adjacent:
                node_in_graph_2 = find_node(colored_graph, node)

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

            if fault:
                break
        verified = validity_check(colored_graph)
        if not verified:
            colored_graph = reset_graph(colored_graph)
            trees = reset_graph(trees)
    return colored_graph


def test_graph():
    graph = [Node("A", ["B", "C", "D"]),
             Node("B", ["A", "D"]),
             Node("C", ["A", "D"]),
             Node("D", ["A", "B", "C", "E"]),
             Node("E", ["D"]),
             Node("F")]
    return graph


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


def remove_cutset(graph):
    cutset = []
    rest = copy.deepcopy(graph)

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

    while True:
        if len(rest) == 0:
            break
        largest_deg_node = None
        for node in rest:
            if largest_deg_node is None:
                largest_deg_node = node
            elif node.get_degree() > largest_deg_node.get_degree():
                largest_deg_node = node
        rest.remove(largest_deg_node)
        cutset.append(largest_deg_node.name)
        for adjacent_node in largest_deg_node.adjacent:
            find_node(rest, adjacent_node).remove_adjacent(largest_deg_node.name)
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
    return cutset


def main():
    graph = usa_graph()

    cutset = remove_cutset(graph)
    trees = copy.deepcopy(graph)

    for node in cutset:
        trees = remove_node_from_graph(trees, node)
    colored = color(cutset, trees, graph)
    for node in colored:
        node.print()


if __name__ == "__main__":
    main()
