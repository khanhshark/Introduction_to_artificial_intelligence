from collections import defaultdict
from queue import Queue, PriorityQueue


def BFS(graph, start, end):
    visited = []  # Danh sách lưu các đỉnh đã thăm
    frontier = Queue()  # Hàng đợi cho các đỉnh cần thăm
    if not graph:  
        raise Exception("No path found")
    # Thêm đỉnh bắt đầu vào hàng đợi và danh sách đã thăm
    frontier.put(start)
    visited.append(start)

    # Khởi tạo từ điển cha cho từng đỉnh
    parent = dict()
    parent[start] = None
    path_found = False

    while True:
        # Kiểm tra xem hàng đợi có trống không
        if frontier.empty():
            raise Exception("No path found")

        # Lấy đỉnh hiện tại từ hàng đợi
        current_node = frontier.get()
        visited.append(current_node)    
     
        # Kiểm tra xem đỉnh hiện tại có phải là đỉnh đích không
        if current_node == end:
            path_found = True
            break
       
        # Duyệt qua các đỉnh kề của đỉnh hiện tại
        for node in graph[current_node]:
            if node not in visited:
                frontier.put(node)  # Thêm đỉnh vào hàng đợi
                parent[node] = current_node  # Gán đỉnh cha
                visited.append(node)  # Đánh dấu đỉnh là đã thăm
       
        
    # Xây dựng đường đi
    path = []
    if path_found:
        path.append(end)  # Thêm đỉnh đích vào đường đi
        while parent[end] is not None:  # Lần ngược từ đỉnh đích tới đỉnh bắt đầu
            path.append(parent[end])
            end = parent[end]
        path.reverse()  # Đảo ngược đường đi để từ đỉnh bắt đầu đến đỉnh đích

    return path  # Trả về đường đi





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
    with open("input.txt", "r") as file:
        size, start, goal, matrix = read_txt(file)
   
    # Chuyển ma trận kề thành danh sách kề
    graph = convert_graph(matrix)

    # Gọi hàm BFS để tìm đường đi từ đỉnh start đến đỉnh goal
    try:
        path = BFS(graph, start, goal)
        print("Đường đi tìm thấy:", path)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()
    

