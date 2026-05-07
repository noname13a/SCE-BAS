class Graph:
    def __init__(self, size):
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.size = size
        self.vertex_index = [''] * size
        self.vertex_data = [''] * size

    def add_edge(self, u, v):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = 1

    def add_vertex(self, vertex, index, title):
        if 0 <= vertex < self.size:
            self.vertex_index[vertex] = index
            self.vertex_data[vertex] = title
            
    def print_graph(self):
        print("Adjacency Matrix:")
        for row in self.adj_matrix:
            print(' '.join(map(str, row)))
        print("\nVertex Data:")
        for vertex, data in enumerate(self.vertex_index):
            print(f"Vertex {vertex}: {data}", self.vertex_data[vertex]['title'])
            
    def dfs_util(self, v, visited, nodes):
        #print(self.vertex_index[v], self.vertex_data[v]['title'])
        visited[v] = 1
        for i in range(self.size):
            if self.adj_matrix[v][i] == 1:
                cont = 0
                for j in range(self.size):
                    if self.adj_matrix[j][i] and not visited[j]:
                        cont = cont + 1
                if(cont<1):
                    nodes.append([["node"+str(i)],[self.vertex_data[i]["identifier"]],self.vertex_data[i]['title']])
                    self.dfs_util(i, visited, nodes)
                
    def dfs_util_max_min(self, v, visited):
        marked = 1
        #print("\n" + self.vertex_index[v], self.vertex_data[v]['title'])
        for line in enumerate(self.adj_matrix):
            if(line[1][v]):
                #marked = 0
                continue
        visited[v] = marked
        for i in range(self.size):
            if self.adj_matrix[v][i] == 1 and not visited[i]:
                self.dfs_util_max_min(i, visited)
                
    def dfs(self, start_vertex_data):
        visited = [False] * self.size
        nodes = []
        nodes.append([["node0"],[self.vertex_data[0]["identifier"]],self.vertex_data[0]['title']])
        start_vertex = self.vertex_index.index(start_vertex_data)
        self.dfs_util(start_vertex, visited, nodes)
        #self.dfs_util_max_min(start_vertex, visited)
        return nodes

#g.print_graph()