import csv

# Tablica obiektów
node_tab = []

class Node:
    def __init__(self, name, length, predecessor):
        self.name = name
        self.length = float(length)
        self.predecessor = predecessor  # lista nazw lub obiektów
        self.ES = 0  # Early Start
        self.EF = 0  # Early Finish
        self.LS = float('inf')  # Late Start
        self.LF = float('inf')  # Late Finish

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

# Zamiana nazw poprzedników na obiekty
name_to_node = {node.name: node for node in node_tab}
for node in node_tab:
    node.predecessor = [name_to_node[p] for p in node.predecessor if p in name_to_node]

# Obliczanie ES i EF (forward pass)
for node in node_tab:
    if not node.predecessor:
        node.ES = 0
    else:
        node.ES = max(pred.EF for pred in node.predecessor)
    node.EF = node.ES + node.length

# Obliczanie LF i LS (backward pass)
# Szukamy maksymalnego EF jako koniec projektu
max_EF = max(node.EF for node in node_tab)
for node in node_tab:
    if not any(node in other.predecessor for other in node_tab):  # jeśli nie jest poprzednikiem dla nikogo
        node.LF = max_EF
        node.LS = node.LF - node.length

# Iterujemy odwrotnie, aby propagować czasy do przodków
for node in reversed(node_tab):
    for pred in node.predecessor:
        pred.LF = min(pred.LF, node.LS)
        pred.LS = pred.LF - pred.length
