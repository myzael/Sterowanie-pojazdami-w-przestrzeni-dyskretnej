from PIL import Image
import networkx as nx

class reader(object):
    '''
    Reads board from B&W bmp file using under the following assumptions
    '''

    def read(self, filename, resolution=1):
        '''
        Reads the image
        '''
        im = Image.open(filename)
        im = im.rotate(270)
        size = im.size
        a = im.load()
        g = nx.grid_2d_graph(size[1], size[0])
        
        # fill the diagonal vertices
        for i in xrange(0, size[0]):
            for j in xrange(0, size[1]):
                if i > 0 and j > 0:
                    g.add_edge((i, j), (i - 1, j - 1))
                if i < size[0]-1 and j > 0:
                    g.add_edge((i, j), (i + 1, j - 1))
                if i > 0 and j < size[1]-1:
                    g.add_edge((i, j), (i - 1, j + 1))
                if i < size[0]-1 and j < size[1]-1:
                    g.add_edge((i, j), (i + 1, j + 1))
                    
        for i in xrange(0, size[0]):
            for j in xrange(0, size[1]):
                if(a[j, i] == 0):
                    g.remove_node((i, j))
        pos = {}
        for pair in g.nodes():
            pos[pair] = pair
         
        return {'g':g, 'pos':pos}
                
            
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    br = reader()
    
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

