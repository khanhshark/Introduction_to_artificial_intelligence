from queue import Queue, PriorityQueue
from collections import defaultdict


class Graph:
    def __init__(self):
        self.adjancy_matrix = None # ma trận kề
        self.adjancy_list = None # danh sách kề
        self.start_node = None # node bắt đầu 
        self.end_node = None # node kết thúc
        self.has_weight = False # ma trận có trọng số hay không 
        self.size = 0 # kích thước của ma trận
        
    def read_file_text(self, file_name="input.txt"):
        file = open(file_name, "r")
        self.size = int(file.readline())
        self.start_node, self.end_node = [int(num) for num in file.readline().split(' ')]
        # ma trận 
        self.adjancy_matrix = [[int(num) for num in file.readline().split(' ')] for num in range(self.size)]
        return self.size, self.start_node, self.end_node, self.adjancy_matrix
    
    def convert_to_list(self, weight=None):
        self.adjancy_list = defaultdict(list)
        for i in range(len(self.adjancy_matrix)):
            for j in range(len(self.adjancy_matrix[i])):
                    # Đồ thị không trọng số
                if self.adjancy_matrix[i][j] == 1 and weight is None:
                    self.adjancy_list[i].append(j)
                # Đồ thị có trọng số
                if self.adjancy_matrix[i][j] != 0 and weight is not None:
                    self.adjancy_list[i].append((j, self.adjancy_matrix[i][j]))
                    self.has_weight = True
        return self.adjancy_list
        
    def bfs(self, start_node, end_node):
        if not self.adjancy_list:  #! Kiểm tra xem adjacency_list có rỗng không
            raise Exception("No path found")
        visited = []
        frontier = Queue()
        frontier.put(start_node)
        visited.append(start_node)
        parent = dict()
        parent[start_node] = None
        path_found = False
        while True:
            if frontier.empty():
                raise Exception("No path found")
            current_node = frontier.get()
            visited.append(current_node) 

            if current_node == end_node:
                path_found = True
                break
            for node in self.adjancy_list[current_node]:
                if node not in visited:
                    frontier.put(node)
                    parent[node] = current_node
                    visited.append(node)
        
        path = []
        if path_found:
            path.append(end_node)
            while parent[end_node] is not None:
                path.append(parent[end_node])
                end_node = parent[end_node]
            path.reverse()

        return path
    def dfs(self, start_node, end_node):
        if not self.adjancy_list:  #! Kiểm tra xem adjacency_list có rỗng không
            raise Exception("No path found")
        visited = []
        frontier = []

        frontier.append(start_node)
        visited.append(start_node)

        parent = dict()
        parent[start_node] = None

        path_found = False
        while True:
            if frontier == []:
                raise Exception("No path found")
            current_node = frontier.pop()
            visited.append(current_node)

            if current_node == end_node:
                path_found = True
                break

            for node in self.adjancy_list[current_node]:
                if node not in visited:
                    frontier.append(node)
                    parent[node] = current_node
                    visited.append(node)

        path = []
        if path_found:
            path.append(end_node)
            while parent[end_node] is not None:
                path.append(parent[end_node])
                end_node = parent[end_node]
            path.reverse()

        return path
    
    def ucs(self, start_node, end_node):
        if not self.adjancy_list:  #! Kiểm tra xem adjacency_list có rỗng không
            raise Exception("No path found")
        visited = []
        frontier = PriorityQueue()

        frontier.put((0, start_node))
        visited.append(start_node)

        parent = dict()
        parent[start_node] = None
        current_weight = 0 #! nên khởi tạo ra trước
        path_found = False
        
        while True:
            if frontier.empty():
                raise Exception("No path found")
            current_weight, current_node = frontier.get()
            visited.append(current_node)

            if current_node == end_node:
                path_found = True
                break

            for node_i in self.adjancy_list[current_node]:
                node, weight = node_i
                if node not in visited:
                    frontier.put((current_weight + weight, node))
                    parent[node] = current_node
                    visited.append(node)

        path = []
        if path_found:
            path.append(end_node)
            while parent[end_node] is not None:
                path.append(parent[end_node])
                end_node = parent[end_node]
            path.reverse()

        return path, current_weight
