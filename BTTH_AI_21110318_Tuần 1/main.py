from graph import *

if __name__ == '__main__':
    try:
        # Tạo đồ thị từ tệp đầu vào
        graph_new_1 = Graph()
        graph_new_1.read_file_text("input.txt")
        adjList_1 = graph_new_1.convert_to_list()
        # Thực hiện BFS
        bfs_1_path = graph_new_1.bfs(graph_new_1.start_node, graph_new_1.end_node)
        print("BFS path: ", bfs_1_path)
        # Thực hiện DFS
        dfs_1_path = graph_new_1.dfs(graph_new_1.start_node, graph_new_1.end_node)
        print("DFS path: ", dfs_1_path)
        # Tạo đồ thị từ tệp UCS
        graph_new_2 = Graph()
        graph_new_2.read_file_text("input_ucs.txt")
        adjList_2 = graph_new_2.convert_to_list(weight=True)
        # Thực hiện UCS
        ucs_2_path, ucs_2_min_weight = graph_new_2.ucs(graph_new_2.start_node, graph_new_2.end_node)
        print("UCS path: ", ucs_2_path, "\nwith min weight: ", ucs_2_min_weight)

    except FileNotFoundError:
        print("Lỗi: Không tìm thấy tệp đầu vào.")
    except Exception as e:
        print(f"Lỗi xảy ra: {e}")