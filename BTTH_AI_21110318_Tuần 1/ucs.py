from queue import PriorityQueue
from collections import defaultdict
def ucs(graph, start, end):
    visited = []
    frontier = PriorityQueue()
    if not graph:  
        raise Exception("No path found")
    # Them node start vao frontier va visited
    frontier.put((0, start))
    visited.append(start)

    # Node start khong co node cha
    parent = dict()
    parent[start] = None
    current_weight = 0 #! nên khởi tạo ra trước
    path_found = False
    while True:
        if frontier.empty():
            raise Exception("No path found")
       
        current_weight, current_node = frontier.get()
        visited.append(current_node)

        # Kiem tra current_node co la node end khong
        if current_node == end:
            path_found = True
            break
   
        for node_i in graph[current_node]:
            node, weight = node_i
            if node not in visited:
                frontier.put((current_weight + weight, node))
                parent[node] = current_node
            
                visited.append(node)
        
    # Xay dung duong di
    path = []
    if path_found:
        path.append(end)
        while parent[end] is not None:
            path.append(parent[end])
            end = parent[end]
        path.reverse()
    
    return current_weight, path


# Đọc dữ liệu từ file txt
def read_txt(file):
    size = int(file.readline())
    start, goal = [int(num) for num in file.readline().split()]
    matrix = [[int(num) for num in line.split()] for line in file]
    return size, start, goal, matrix

# Chuyển ma trận kề thành danh sách kề (danh sách các đỉnh kề)
def convert_graph(matrix):
    adjList = defaultdict(list)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:  # Giả sử 1 biểu thị có đường nối
                adjList[i].append(j)
    return adjList

# Chuyển ma trận trọng số thành danh sách kề có trọng số
def convert_graph_weight(matrix):
    adjList = defaultdict(list)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != 0:  # Giả sử 0 là không có đường nối
                adjList[i].append((j, matrix[i][j]))  # Thêm cặp (đỉnh, trọng số)
    return adjList
def main():
    # Đọc dữ liệu từ tệp input.txt
    with open("input_ucs.txt", "r") as file:
        size, start, goal, matrix = read_txt(file)
   
    # Chuyển ma trận kề thành danh sách kề
    graph = convert_graph_weight(matrix)
    # Gọi hàm BFS để tìm đường đi từ đỉnh start đến đỉnh goal
    try:
        path = ucs(graph, start, goal)
        print("Đường đi tìm thấy:", path)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()