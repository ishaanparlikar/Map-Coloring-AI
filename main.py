class Node:
    def __init__(self, name, adjacent=[]):
        self.name = name
        self.adjacent = adjacent
        self.colorPicked = None
        self.possibleColors = ["R", "B", "G", "Y"]

    def remove_adjacent(self, node):
        if node in self.adjacent:
            self.adjacent.remove(node)

    def remove_color(self, color):
        if color in self.possibleColors:
            self.possibleColors.remove(color)


def main():
    graph = [Node("A", ["B", "C", "D"]),
             Node("B", ["A", "D"]),
             Node("C", ["A", "D"]),
             Node("D", ["A", "B", "C", "E"]),
             Node("E", ["D"]),
             Node("F")]


if __name__ == "__main__":
    main()