import csv

# Tablica obiektów
node_tab = []

class Node:
    def __init__(self, name, length, predecessor):
        self.name = name
        self.length = float(length)
        self.predecessor = predecessor  # lista nazw lub obiektów

    def __repr__(self):
        return f"Node({self.name}, {self.length}, {[p.name if isinstance(p, Node) else p for p in self.predecessor]})"

# Etap 1: wczytywanie z pliku – jeszcze bez zamiany nazw na obiekty
with open('zadania.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row['ac']
        length = row['du']
        raw_pr = row['pr']

        if raw_pr == "-" or not raw_pr:
            predecessors = []
        else:
            predecessors = list(raw_pr)  # np. "AB" → ["A", "B"]

        node = Node(name, length, predecessors)
        node_tab.append(node)


name_to_node = {node.name: node for node in node_tab}
for node in node_tab:
    node.predecessor = [name_to_node[p] for p in node.predecessor if p in name_to_node]


