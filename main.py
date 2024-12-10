
from comment_tree import CommentTree, print_comment_tree

# Создание дерева комментариев
tree = CommentTree()

def start():

    # Добавление комментариев
    tree.add_comment(1, "Root comment", "Alice")
    tree.add_comment(2, "Reply to root", "Bob", parent_id=1)
    tree.add_comment(3, "Another reply", "Charlie", parent_id=1)
    tree.add_comment(4, "Nested reply", "Dave", parent_id=2)
    tree.add_comment(5, "Further nested reply", "Eve", parent_id=4)
    tree.add_comment(6, "Sibling reply to nested", "Frank", parent_id=2)
    tree.add_comment(7, "Deeply nested reply", "Grace", parent_id=5)
    tree.add_comment(8, "Another root-level comment", "Hank")
    tree.add_comment(9, "Reply to another root-level comment", "Ivy", parent_id=8)
    tree.add_comment(10, "Nested under Ivy", "Jack", parent_id=9)
    tree.add_comment(11, "Another reply to Ivy", "Ken", parent_id=9)
    tree.add_comment(12, "Reply to Charlie", "Liam", parent_id=3)
    tree.add_comment(13, "Further nesting under Ken", "Mia", parent_id=11)
    tree.add_comment(14, "Another deeply nested reply", "Nina", parent_id=13)
    tree.add_comment(15, "Sibling to deeply nested", "Oscar", parent_id=13)
    tree.add_comment(16, "Independent root-level comment", "Pam")
    tree.add_comment(17, "Reply to Pam", "Quincy", parent_id=16)


if __name__ == '__main__':
    
    start()

    # Вывод комментариев по глубине (DFS)
    tree.print_dfs(start_id=1)

    # Вывод комментариев по ширине (BFS)
    tree.print_bfs(start_id=1)

    tree.delete_comment(4)

    # Экспорт в JSON
    json_data = tree.to_json(filename='file.json', save_to_file=True)
    xml_data = tree.to_xml(filename='file.xml', save_to_file=True)

    # Импорт из JSON
    tree.from_json(json_data)
    print("\nИмпортированное дерево:")
    print_comment_tree(tree)
    print('\n\n\n')

    tree.from_xml(xml_data)
    print("\nИмпортированное дерево:")
    print_comment_tree(tree)