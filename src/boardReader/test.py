import networkx as nx
import matplotlib.pyplot as plt
from boardReader import BoardReader

br = BoardReader()

G = br.read('test.bmp')
nx.draw_networkx_edges(G['g'], G['pos'])
nx.draw_networkx_nodes(G['g'], G['pos'], node_size=50)
plt.savefig("test-results.png")
plt.show()

G = br.read('test2.bmp')
nx.draw_networkx_edges(G['g'], G['pos'])
nx.draw_networkx_nodes(G['g'], G['pos'], node_size=50)
plt.savefig("test2-results.png")
plt.show()
