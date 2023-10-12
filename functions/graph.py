import sys

class Graph:
  def __init__(self):
    self.vertexs = {}
    self.edges = []


  def add_vertex(self, id, name, image):
    self.vertexs[id] = {
      'id': id,
      'name': name,
      'image': image,
      'neighbors': []
    }

  def add_edge(self, origin, destiny):
    self.edges.append([origin, destiny])
    self.vertexs[origin]['neighbors'].append(destiny)

  def vertex_exists(self, id):
    if self.vertexs.get(id):
      return True
    return False

  def get_plot_data(self):
    vertexs_list = []
    for vertex in self.vertexs:
      data = {
        'id': vertex,
        'name': self.vertexs[vertex]['name'],
        'image': self.vertexs[vertex]['image'],
        'shape': 'circularImage',
        'label': ''
      }
      vertexs_list.append(data)

    edges_list = []

    for edge in self.edges:
      data = {
        'from': edge[0],
        'to': edge[1]
      }
      edges_list.append(data)

    graph = {
      'nodes': vertexs_list,
      'edges': edges_list
    }

    return graph
  
  def get_vertex(self, id):
    return self.vertexs[id]
  
  def get_neighbors(self, vertex):
    return self.vertexs[vertex]['neighbors']
  
  def shortest_path(self, origin, destiny, tree):
    print(tree, file=sys.stderr)
    path = []
    current = destiny
    while current != origin:
      path.append(current)
      current = tree[current]['parent']
    path.append(origin)
    return path[::-1]

  

  def bfs(self, origin, destiny):
    tree = {}
    tree[origin] = {
      'id': origin,
      'parent': None,
      'distance': 0,
      'sons': []
    }
    visited = [origin]
    queue = [origin]
    while len(queue) > 0:
      current = queue.pop(0)
      neighbors = self.get_neighbors(current)
      tree[current]['sons'] = neighbors
      for neighbor in neighbors:
        if neighbor not in visited:
          visited.append(neighbor)
          queue.append(neighbor)
          tree[neighbor] = {
            'id': neighbor,
            'parent': current,
            'distance': tree[current]['distance'] + 1,
            'sons': []
          }
        if neighbor.lower() == destiny.lower():
          return self.shortest_path(origin, destiny, tree)

    
    return []

