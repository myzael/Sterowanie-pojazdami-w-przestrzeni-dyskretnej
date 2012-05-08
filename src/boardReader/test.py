import BoardReader
import networkx as nx
import matplotlib.pyplot as plt

br = BoardReader()

G = br.read('test.bmp')
nx.draw_networkx_edges(G['g'], G['pos'])
nx.draw_networkx_nodes(G['g'], G['pos'], node_size=50)
plt.show()

G = br.read('test2.bmp')
nx.draw_networkx_edges(G['g'], G['pos'])
nx.draw_networkx_nodes(G['g'], G['pos'], node_size=50)
plt.show()
