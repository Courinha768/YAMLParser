import unittest
import yaml

class TestYAMLParser(unittest.TestCase):
	def test_basic_yaml(self):
		yaml_text = """
        name: John Doe
        age: 30
        """
		self.assertEqual(yaml.loads(yaml_text), {'name': 'John Doe', 'age': 30})

	def test_nested_yaml(self):
		yaml_text = """
        person:
          name: Alice
          age: 25
        """
		self.assertEqual(yaml.loads(yaml_text), {"person": {"name": "Alice", "age": 25}})

	def test_list_yaml(self):
		yaml_text = """
        items:
          - apple
          - banana
        """
		self.assertEqual(yaml.loads(yaml_text), {"items": ["apple", "banana"]})

	def test_reference_yaml(self):
		yaml_text = """
        address:
          city: New York
          zip: 10001
        ref_example:
          $ref: "#address"
        """
		self.assertEqual(yaml.loads(yaml_text), {"city": "New York", "zip": 10001})

	def test_boolean_and_null_yaml(self):
		yaml_text = """
        is_active: true
        is_deleted: false
        data: null
        """
		self.assertEqual(yaml.loads(yaml_text), {"is_active": True, "is_deleted": False, "data": None})


if __name__ == "__main__":
	unittest.main()