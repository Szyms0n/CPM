from pyvis.network import Network
from Node import *

net = Network(height='1000px', width='100%', directed=True)
net.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=200)

for node in node_tab:
    czas = int(node.length)

    # Krytyczne zadania: ES == LS
    if int(node.ES) == int(node.LS):
        color = "#e61919"  # czerwony
    else:
        color = "#006400"  # standardowy pomarańczowy

    label_text = (
        f"{node.name}\n"
        f"T={czas}\n"
        f"ES={int(node.ES)}\n"
        f"EF={int(node.EF)}\n"
        f"LS={int(node.LS)}\n"
        f"LF={int(node.LF)}"
    )

    net.add_node(
        node.name,
        label=label_text,
        title=f"Długość: {node.length}",
        color=color
    )

    for PR in node.predecessor:
        # Czy obie strony mają Slack == 0 (czyli ES == LS)
        is_critical_edge = (
                int(PR.ES) == int(PR.LS) and
                int(node.ES) == int(node.LS) and
                int(node.ES) == int(PR.EF)  # ważne: zależność czasowa
        )

        net.add_edge(
            PR.name,
            node.name,
            color="red" if is_critical_edge else "#b08869",  # ciemna dla niekrytycznych
            width=3 if is_critical_edge else 1
        )
net.show('graph.html', notebook=False)
