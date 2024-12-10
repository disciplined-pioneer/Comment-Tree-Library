
from comment_tree import CommentTree, print_comment_tree

def indents():
    print('-'*50)
    print('\n')

def main():

    # Инициализация дерева комментариев
    tree = CommentTree()

    # Добавляем комментарии
    print("Добавление комментариев...")
    tree.add_comment(1, "Это первый комментарий", "Алиса")
    tree.add_comment(2, "Это ответ на первый комментарий", "Боб", parent_id=1)
    tree.add_comment(3, "Это ответ второго уровня", "Чарли", parent_id=2)
    tree.add_comment(4, "Ещё один комментарий на верхнем уровне", "Давид")
    indents()

    # Выводим дерево комментариев с помощью обхода в глубину (DFS)
    print("\nОбход дерева комментариев в глубину (DFS):")
    tree.print_dfs(1)
    indents()

    # Выводим дерево комментариев с помощью обхода в ширину (BFS)
    print("\nОбход дерева комментариев в ширину (BFS):")
    tree.print_bfs(1)
    indents()

    # Обновляем комментарий
    print("\nОбновление комментария с ID 2...")
    tree.update_comment(2, text="Обновлённый ответ на первый комментарий", author="Обновлённый Боб")
    tree.print_dfs(1)
    indents()

    # Удаляем комментарий
    print("\nУдаление комментария с ID 3...")
    tree.delete_comment(3)
    tree.print_dfs(1)
    indents()

    # Сериализуем дерево комментариев в формат JSON и сохраняем в файл
    print("\nСериализация дерева комментариев в формат JSON:")
    json_data = tree.to_json(save_to_file=True)
    indents()

    # Сериализуем дерево комментариев в формат XML и сохраняем в файл
    print("\nСериализация дерева комментариев в формат XML:")
    xml_data = tree.to_xml(save_to_file=True)
    indents()

    # Загружаем дерево из данных в формате JSON
    print("\nЗагрузка дерева из JSON:")
    tree_from_json = CommentTree()
    tree_from_json.from_json(json_data)
    tree_from_json.print_dfs(1)
    indents()

    # Загружаем дерево из данных в формате XML
    print("\nЗагрузка дерева из XML:")
    tree_from_xml = CommentTree()
    tree_from_xml.from_xml(xml_data)
    tree_from_xml.print_dfs(1)
    indents()

    # Выводим дерево комментариев в красивом виде
    print_comment_tree(tree)
    indents()

if __name__ == "__main__":
    main()