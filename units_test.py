import unittest
import os
import json
from io import StringIO
from unittest.mock import patch
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element


from comment_tree import CommentTree
import unittest
from io import StringIO
from unittest.mock import patch
import json
import xml.etree.ElementTree as ET
from comment_tree import CommentTree

class TestCommentTree(unittest.TestCase):

    def setUp(self):
        # Создаем новый экземпляр дерева комментариев перед каждым тестом
        self.tree = CommentTree()

    def test_add_comment(self):
        # Добавление нового комментария
        self.tree.add_comment(1, "First comment", "Alice")
        self.assertEqual(len(self.tree.nodes), 1)
        self.assertEqual(self.tree.nodes[1].text, "First comment")

    def test_add_comment_with_parent(self):
        # Добавление комментария с родительским элементом
        self.tree.add_comment(1, "First comment", "Alice")
        self.tree.add_comment(2, "Reply to first", "Bob", parent_id=1)
        self.assertEqual(len(self.tree.nodes), 2)
        self.assertEqual(self.tree.nodes[2].parent_id, 1)

    def test_add_comment_with_invalid_parent(self):
        # Попытка добавить комментарий с несуществующим родителем
        with self.assertRaises(ValueError):
            self.tree.add_comment(2, "Invalid parent", "Bob", parent_id=999)

    def test_delete_comment(self):
        # Удаление комментария
        self.tree.add_comment(1, "First comment", "Alice")
        self.tree.delete_comment(1)
        self.assertEqual(len(self.tree.nodes), 0)

    def test_delete_non_existent_comment(self):
        # Попытка удалить несуществующий комментарий
        with self.assertRaises(ValueError):
            self.tree.delete_comment(999)

    def test_update_comment(self):
        # Обновление комментария
        self.tree.add_comment(1, "First comment", "Alice")
        self.tree.update_comment(1, text="Updated comment", author="Bob")
        self.assertEqual(self.tree.nodes[1].text, "Updated comment")
        self.assertEqual(self.tree.nodes[1].author, "Bob")

    def test_update_non_existent_comment(self):
        # Попытка обновить несуществующий комментарий
        with self.assertRaises(ValueError):
            self.tree.update_comment(999, text="Updated text")

    def test_traverse_dfs(self):
        # Тестирование DFS (глубина)
        self.tree.add_comment(1, "Root comment", "Alice")
        self.tree.add_comment(2, "Child comment", "Bob", parent_id=1)
        output = StringIO()
        with patch('sys.stdout', new=output):
            self.tree.traverse_dfs(1, lambda node: print(node.text))
        output.seek(0)
        self.assertIn("Root comment", output.getvalue())
        self.assertIn("Child comment", output.getvalue())

    def test_traverse_bfs(self):
        # Тестирование BFS (ширина)
        self.tree.add_comment(1, "Root comment", "Alice")
        self.tree.add_comment(2, "Child comment", "Bob", parent_id=1)
        output = StringIO()
        with patch('sys.stdout', new=output):
            self.tree.traverse_bfs(1, lambda node: print(node.text))
        output.seek(0)
        self.assertIn("Root comment", output.getvalue())
        self.assertIn("Child comment", output.getvalue())

    def test_to_json(self):
        # Тестирование преобразования дерева в JSON
        self.tree.add_comment(1, "Root comment", "Alice")
        json_output = self.tree.to_json(save_to_file=False)
        self.assertIn('"comment_id": 1', json_output)

    def test_from_json(self):
        # Тестирование загрузки данных из JSON
        json_data = '[{"comment_id": 1, "text": "Root comment", "author": "Alice", "parent_id": null, "children": []}]'
        self.tree.from_json(json_data)
        self.assertEqual(self.tree.nodes[1].text, "Root comment")

    def test_to_xml(self):
        # Тестирование преобразования дерева в XML
        self.tree.add_comment(1, "Root comment", "Alice")
        xml_output = self.tree.to_xml(save_to_file=False)
        self.assertIn('<comment id="1"', xml_output)

    def test_from_xml(self):
        # Тестирование загрузки данных из XML
        xml_data = '<comments><comment id="1" author="Alice" parent_id="None"><text>Root comment</text></comment></comments>'
        self.tree.from_xml(xml_data)
        self.assertEqual(self.tree.nodes[1].text, "Root comment")

    def test_invalid_json(self):
        # Тестирование обработки ошибок при неверном формате JSON
        with self.assertRaises(json.JSONDecodeError):
            self.tree.from_json('invalid json')

    def test_invalid_xml(self):
        # Тестирование обработки ошибок при неверном формате XML
        invalid_xml = '<comments><comment id="1" author="Alice"><text>Root comment</text></comments>'
        with self.assertRaises(ET.ParseError):
            self.tree.from_xml(invalid_xml)


if __name__ == '__main__':
    # Запуск тестов с подробным выводом
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
