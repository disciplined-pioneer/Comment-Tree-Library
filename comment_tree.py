import os
import json
from collections import deque
import xml.etree.ElementTree as ET
from typing import Callable, Optional

class CommentNode:
    """
    Represents a single comment node in the comment tree.
    Supports conversion to/from dictionaries, XML, and serializing data.
    """
    
    def __init__(self, comment_id: int, text: str, author: str, parent_id: Optional[int] = None):
        """
        Initializes a CommentNode object.

        Args:
            comment_id (int): Unique identifier for the comment.
            text (str): The content of the comment.
            author (str): The author of the comment.
            parent_id (Optional[int]): The ID of the parent comment (if any).
        """
        self.comment_id = comment_id
        self.text = text
        self.author = author
        self.parent_id = parent_id
        self.children = []

    def to_dict(self):
        """
        Converts the CommentNode and its children to a dictionary representation.

        Returns:
            dict: A dictionary representing the comment node.
        """
        return {
            'comment_id': self.comment_id,
            'text': self.text,
            'author': self.author,
            'parent_id': self.parent_id,
            'children': [child.to_dict() for child in self.children]
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a CommentNode from a dictionary.

        Args:
            data (dict): The dictionary containing comment data.

        Returns:
            CommentNode: A newly created CommentNode object.
        """
        node = CommentNode(data['comment_id'], data['text'], data['author'], data['parent_id'])
        for child_data in data['children']:
            child_node = CommentNode.from_dict(child_data)
            node.children.append(child_node)
        return node

    def to_xml(self):
        """
        Converts the CommentNode and its children into XML format as an ElementTree.Element.

        Returns:
            Element: The XML element representing the comment node.
        """
        comment_element = ET.Element('comment', id=str(self.comment_id), author=self.author, parent_id=str(self.parent_id))
        text_element = ET.SubElement(comment_element, 'text')
        text_element.text = self.text
        
        for child in self.children:
            comment_element.append(child.to_xml())
        
        return comment_element

    @staticmethod
    def from_xml(element):
        """
        Converts an XML element into a CommentNode.

        Args:
            element (Element): The XML element representing the comment.

        Returns:
            CommentNode: A newly created CommentNode object.
        """
        comment_id = int(element.attrib['id'])
        author = element.attrib['author']
        
        parent_id_str = element.attrib.get('parent_id', 'None')
        parent_id = None if parent_id_str == 'None' else int(parent_id_str)
        
        text = element.find('text').text
        node = CommentNode(comment_id, text, author, parent_id)
        
        # Recursively add child comments
        for child_element in element.findall('comment'):
            node.children.append(CommentNode.from_xml(child_element))
        
        return node

class CommentTree:
    """
    Represents a tree structure of comments, supporting operations like adding, deleting, updating, and serializing comments.
    """

    def __init__(self):
        """
        Initializes an empty CommentTree.
        """
        self.nodes = {}

    def add_comment(self, comment_id: int, text: str, author: str, parent_id: Optional[int] = None):
        """
        Adds a new comment to the tree.

        Args:
            comment_id (int): Unique identifier for the comment.
            text (str): The content of the comment.
            author (str): The author of the comment.
            parent_id (Optional[int]): The ID of the parent comment (if any).

        Raises:
            ValueError: If the comment ID already exists or if the parent ID is not found.
        """
        if comment_id in self.nodes:
            raise ValueError(f"Comment ID {comment_id} already exists.")
        new_node = CommentNode(comment_id, text, author, parent_id=parent_id)
        self.nodes[comment_id] = new_node
        if parent_id is not None:
            if parent_id not in self.nodes:
                raise ValueError(f"Parent ID {parent_id} does not exist.")
            self.nodes[parent_id].children.append(new_node)

    def delete_comment(self, comment_id: int):
        """
        Deletes a comment from the tree.

        Args:
            comment_id (int): The ID of the comment to delete.

        Raises:
            ValueError: If the comment ID is not found.
        """
        if comment_id not in self.nodes:
            raise ValueError(f"Comment ID {comment_id} does not exist.")
        node = self.nodes[comment_id]
        if node.parent_id is not None:
            parent = self.nodes[node.parent_id]
            parent.children = [child for child in parent.children if child.comment_id != comment_id]
        del self.nodes[comment_id]

    def update_comment(self, comment_id: int, text: Optional[str] = None, author: Optional[str] = None):
        """
        Updates an existing comment's content or author.

        Args:
            comment_id (int): The ID of the comment to update.
            text (Optional[str]): New content for the comment.
            author (Optional[str]): New author for the comment.

        Raises:
            ValueError: If the comment ID is not found.
        """
        if comment_id not in self.nodes:
            raise ValueError(f"Comment ID {comment_id} does not exist.")
        node = self.nodes[comment_id]
        if text:
            node.text = text
        if author:
            node.author = author

    def traverse_dfs(self, start_id: int, action: Callable[[CommentNode], None]):
        """
        Performs a depth-first traversal of the comment tree, applying a provided action to each node.

        Args:
            start_id (int): The ID of the starting comment for traversal.
            action (Callable[[CommentNode], None]): The action to apply to each node.

        Raises:
            ValueError: If the start ID is not found.
        """
        if start_id not in self.nodes:
            raise ValueError(f"Start ID {start_id} does not exist.")
        
        def dfs(node):
            action(node)
            for child in node.children:
                dfs(child)
        
        dfs(self.nodes[start_id])

    def traverse_bfs(self, start_id: int, action: Callable[[CommentNode], None]):
        """
        Performs a breadth-first traversal of the comment tree, applying a provided action to each node.

        Args:
            start_id (int): The ID of the starting comment for traversal.
            action (Callable[[CommentNode], None]): The action to apply to each node.

        Raises:
            ValueError: If the start ID is not found.
        """
        if start_id not in self.nodes:
            raise ValueError(f"Start ID {start_id} does not exist.")
        
        queue = deque([self.nodes[start_id]])
        while queue:
            node = queue.popleft()
            action(node)
            queue.extend(node.children)

    def _add_subtree(self, node):
        """
        Adds a subtree rooted at the given node to the tree. This is a helper method.

        Args:
            node (CommentNode): The root node of the subtree.
        """
        self.nodes[node.comment_id] = node
        for child in node.children:
            self._add_subtree(child)

    def to_json(self, filename: str = "comments_tree.json", save_to_file: bool = True):
        """
        Converts the comment tree to JSON format.

        Args:
            filename (str): The filename to save the data to (if saving to file).
            save_to_file (bool): Whether to save the data to a file (default is True).

        Returns:
            str: The JSON string representing the comment tree.

        Raises:
            ValueError: If the filename is empty.
            FileNotFoundError: If there is an error saving the file.
        """
        try:
            if not filename:
                raise ValueError("Filename cannot be empty.")
            
            if save_to_file:
                data = [node.to_dict() for node in self.nodes.values() if node.parent_id is None]
                project_directory = os.path.dirname(os.path.abspath(__file__))
                filepath = os.path.join(project_directory, filename)
                
                try:
                    with open(filepath, "w", encoding="utf-8") as file:
                        json.dump(data, file, indent=4, ensure_ascii=False)
                    print(f"Data successfully saved to file: {filepath}")
                except OSError as e:
                    raise FileNotFoundError(f"Error saving file: {e}")
            
            return json.dumps([node.to_dict() for node in self.nodes.values() if node.parent_id is None], indent=4)

        except ValueError as ve:
            print(f"Value error: {ve}")
            raise
        except Exception as e:
            print(f"Error processing data: {e}")
            raise

    def from_json(self, data: str):
        """
        Loads the comment tree from a JSON string.

        Args:
            data (str): The JSON string containing comment data.
        """
        nodes_data = json.loads(data)
        self.nodes = {}
        for node_data in nodes_data:
            root_node = CommentNode.from_dict(node_data)
            self._add_subtree(root_node)

    def to_xml(self, filename: str = "comments_tree.xml", save_to_file: bool = True):
        """
        Converts the comment tree to XML format.

        Args:
            filename (str): The filename to save the data to (if saving to file).
            save_to_file (bool): Whether to save the data to a file (default is True).

        Returns:
            str: The XML string representing the comment tree.

        Raises:
            ValueError: If the filename is empty.
            FileNotFoundError: If there is an error saving the file.
        """
        try:
            if not filename:
                raise ValueError("Filename cannot be empty.")
            
            root = ET.Element('comments')
            for node in self.nodes.values():
                if node.parent_id is None:
                    root.append(node.to_xml())
            
            tree = ET.ElementTree(root)
            project_directory = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(project_directory, filename)
            
            if save_to_file:
                tree.write(filepath, encoding="utf-8", xml_declaration=True)
                print(f"Data successfully saved to file: {filepath}")
            
            return ET.tostring(root, encoding="unicode", method="xml")
        except ValueError as ve:
            print(f"Value error: {ve}")
            raise
        except Exception as e:
            print(f"Error processing data: {e}")
            raise

    def from_xml(self, xml_data: str):
        """
        Loads the comment tree from an XML string.

        Args:
            xml_data (str): The XML string containing comment data.
        """
        root_element = ET.fromstring(xml_data)
        for comment_element in root_element.findall('comment'):
            node = CommentNode.from_xml(comment_element)
            self._add_subtree(node)

    def print_dfs(self, start_id: int):
        """
        Prints the comment tree using depth-first traversal.

        Args:
            start_id (int): The ID of the starting comment for traversal.
        """
        def dfs(node, level=0):
            print("    " * level + f"- {node.text} (by {node.author})")
            for child in node.children:
                dfs(child, level + 1)
        
        if start_id not in self.nodes:
            print(f"Start ID {start_id} does not exist.")
            return
        print("DFS:")
        dfs(self.nodes[start_id])

    def print_bfs(self, start_id: int):
        """
        Prints the comment tree using breadth-first traversal.

        Args:
            start_id (int): The ID of the starting comment for traversal.
        """
        if start_id not in self.nodes:
            print(f"Start ID {start_id} does not exist.")
            return
        
        print("BFS:")
        queue = deque([self.nodes[start_id]])
        level = 0
        while queue:
            level_size = len(queue)
            print(f"\nLevel {level}:")
            for _ in range(level_size):
                node = queue.popleft()
                print(f"- {node.text} (by {node.author})")
                queue.extend(node.children)
            level += 1

def print_comment_tree(tree):
    """
    Prints the comment tree in a readable format.

    Args:
        tree (CommentTree): The CommentTree object to print.
    """
    def print_node(node, prefix=""):
        print(f"{prefix}{node.text} (by {node.author})")
        for i, child in enumerate(node.children):
            if i == len(node.children) - 1:
                print_node(child, prefix + "    └── ")
            else:
                print_node(child, prefix + "    ├── ")

    for root_node in [node for node in tree.nodes.values() if node.parent_id is None]:
        print_node(root_node)
