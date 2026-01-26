# Tools loader: Load OpenAPI tools từ YAML
import yaml

def load_api_spec(path: str = "app/tools/apis.yaml"):
    with open(path, 'r') as f:
        return yaml.safe_load(f)
