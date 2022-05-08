class Graph:
  def __init__(self, data):
    self.vertexs = {}
    self.add_vertex(data['username'], data['name'], data['image'])
    self.edges = []


  def add_vertex(self, id, name, image):
    self.vertexs[id] = {
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
      }
      vertexs_list.append(self.vertexs[vertex])

    graph = {
      'vertexs': vertexs_list,
      'edges': self.edges
    }

    return graph

  