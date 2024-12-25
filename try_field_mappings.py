import yaml

with open("field_number_mapping.yml", "r") as file:
    data = yaml.safe_load(file)

print(data)
