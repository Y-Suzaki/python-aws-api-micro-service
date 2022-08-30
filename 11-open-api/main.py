import yaml

with open('base.yml', 'r') as stream:
    yaml_data = yaml.safe_load(stream)
    print(yaml_data)


with open('output/test.yml', 'w', encoding='utf-8', newline='\n') as stream:
    yaml.default_flow_style = False
    yaml.safe_dump(yaml_data, stream=stream, sort_keys=False)
