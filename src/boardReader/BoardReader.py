from PIL import Image
import networkx as nx

class ArgumentError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class BoardReader(object):
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
        if len(im.getcolors()) > 2:
            raise ArgumentError("image is not B&W") 
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
                
            


