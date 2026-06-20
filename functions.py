def load_config(file_name="config.yaml"):
    with open(file_name, encoding="utf-8") as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config
