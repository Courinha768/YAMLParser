import yaml

def main():
	yaml_text = """
	        items:
	          - apple
	          - banana
	        """
	print(yaml.loads(yaml_text))

if __name__ == "__main__":
	main()