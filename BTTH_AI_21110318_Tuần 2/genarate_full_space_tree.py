from collections import deque
import os
# Thiết lập biến môi trường để thêm đường dẫn đến thư mục bin của Graphviz
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
import pydot 
import argparse

options = [(1,0),(0,1),(1,1),(0,2),(2,0)]
Parent = {}
graph = pydot.Dot(graph_type='graph', 
                  strict=False, 
                  bgcolor="#fff3af", 
                  label="fig: Missionaries and Cannibal State Space Tree", 
                  fontcolor="red", 
                  fontsize="24", 
                  overlap="true")

# Thiết lập argparse để nhận đối số từ dòng lệnh
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--depth", required=False, help="Maximum depth up to which you want to generate the State Space Tree")
args = vars(arg_parser.parse_args())

# Lấy độ sâu tối đa từ đối số
# python generate_full_space_tree.py --depth 5 ví dụ
max_depth = int(args.get("depth", 20))

def is_valid_move(number_missionaries, number_cannibals):
    """Kiểm tra xem các ràng buộc về số lượng có được thỏa mãn không."""
    return (0 <= number_missionaries <= 3) and (0 <= number_cannibals <= 3)

def write_image(file_name="state_space"):
    """Ghi hình ảnh đồ thị vào tệp PNG."""
    try:
        graph.write_png(f"{file_name}_{max_depth}.png")
        print(f"File {file_name}_{max_depth}.png successfully written.")
    except Exception as e:
        print("Error while writing file:", e)
        
def draw_edge(number_missionaries, number_cannibals, side, depth_level, node_num):
    u, v = None, None

    # Kiểm tra xem có nút cha không
    if Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)] is not None:
        u = pydot.Node(str(Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)]), 
                       label=str(Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)][:3]))
        graph.add_node(u)

        # Tạo nút cho nút hiện tại
        v = pydot.Node(str((number_missionaries, number_cannibals, side, depth_level, node_num)),
                    label=str((number_missionaries, number_cannibals, side)))
        graph.add_node(v)
        #! kiểm  tra thay Node thành 
        edge = pydot.Edge(str(Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)]),
                            str((number_missionaries, number_cannibals, side, depth_level, node_num)), dir='forward')
        graph.add_edge(edge)
        
    else:
        # For start node
        v = pydot.Node(str((number_missionaries, number_cannibals, side, depth_level, node_num)),
                       label=str((number_missionaries, number_cannibals, side)))
        graph.add_node(v)

    return u, v    


def is_start_state(number_missionaries, number_cannibals, side):
    return (number_missionaries, number_cannibals, side) == (3, 3, 1)


def is_goal_state(number_missionaries, number_cannibals, side):
    return (number_missionaries, number_cannibals, side) == (0, 0, 0)

def number_of_cannibals_exceeds(number_missionaries, number_cannibals):
    number_missionaries_right = 3 - number_missionaries
    number_cannibals_right = 3 - number_cannibals
    return (number_missionaries > 0 and number_missionaries < number_cannibals) \
or (number_missionaries_right > 0 and number_missionaries_right < number_cannibals_right)

i = 0  # Khởi tạo biến toàn cục i
def generate():
    global i
    q = deque()
    node_num = 0
    q.append((3, 3, 1, 0, node_num))

    Parent[(3, 3, 1, 0, node_num)] = None

    while q:
        number_missionaries, number_cannibals, side, depth_level, node_num = q.popleft()
        # print(number_missionaries, number_cannibals)
        # Draw edge from u -> v
        # where u = Parent[v]
        # and v = (number_missionaries, number_cannibals, side, depth_level)
        u, v = draw_edge(number_missionaries, number_cannibals, side, depth_level, node_num)

        if is_start_state(number_missionaries, number_cannibals, side):
            v.set_style("filled")
            v.set_fillcolor("blue")
            v.set_fontcolor("white")
        elif is_goal_state(number_missionaries, number_cannibals, side):
            v.set_style("filled")
            v.set_fillcolor("green")
            continue
            # return True
        elif number_of_cannibals_exceeds(number_missionaries, number_cannibals):
            v.set_style("filled")
            v.set_fillcolor("red")
            continue
        else:
            v.set_style("filled")
            v.set_fillcolor("orange")

        if depth_level == max_depth:
            return True

        op = -1 if side == 1 else 1
        can_be_expanded = False

        # i = node_num
        for x, y in options:
            next_m, next_c, next_s = number_missionaries + op * x, number_cannibals + op * y, int(not side)

            if Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)] is None \
               or (next_m, next_c, next_s) != Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)][:3]:
                if is_valid_move(next_m, next_c):
                    can_be_expanded = True
                    i += 1
                    q.append((next_m, next_c, next_s, depth_level + 1, i))

                    # Keep track of parent
                    Parent[(next_m, next_c, next_s, depth_level + 1, i)] = (number_missionaries, number_cannibals, side, depth_level, node_num)
        
        if not can_be_expanded:
            v.set_style("filled")
            v.set_fillcolor("gray")
    print("No solution found.")
    return False
if __name__ == "__main__":
    if generate():
        write_image()