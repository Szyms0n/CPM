from pyvis.network import Network
from Node import *
net = Network()



net = Network(directed=True)

net = Network(height='1000px', width='100%', directed=True)
net.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=200)


#sigma


for node in node_tab:
    czas = int(node.length)
    label_text = f"{node.name}\nT={czas}\nES=\nEF=\nLS=\nLF="

    net.add_node(node.name, label=label_text, title=f"Długość: {node.length}", color="#d47415")
    for PR in node.predecessor:
        net.add_edge(PR.name, node.name)






net.show('graph.html', notebook=False) \


