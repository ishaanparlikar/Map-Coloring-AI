class Node:
    def __init__(self, name, adjacent=[]):
        self.name = name
        self.adjacent = adjacent
        self.color_picked = None
        self.possible_colors = ["R", "B", "G", "Y"]

    def remove_adjacent(self, node):
        if node in self.adjacent:
            self.adjacent.remove(node)

    def remove_color(self, color):
        if color in self.possible_colors:
            self.possible_colors.remove(color)

#dosent work yet
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
            # print("Found " + node.name)
            return node
    return None


def main():
    print("MAIN")
    test_valid()


def test_valid():
    graph = [Node("A", ["B", "C", "D"]),
             Node("B", ["A", "D"]),
             Node("C", ["A", "D"]),
             Node("D", ["A", "B", "C", "E"]),
             Node("E", ["D"]),
             Node("F")]
    graph[0].color_picked = "R"
    graph[1].color_picked = "B"
    graph[2].color_picked = "G"
    graph[3].color_picked = "Y"
    graph[4].color_picked = "R"
    graph[4].color_picked = "Y"

    print(validity_check(graph))


if __name__ == "__main__":
    main()
