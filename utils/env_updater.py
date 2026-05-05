import json

def update_env_token(env_path, key, value):

    with open(env_path) as f:
        env = json.load(f)

    updated = False

    for var in env["values"]:
        if var["key"] == key:
            var["value"] = value
            updated = True

    # If key not found → add it
    if not updated:
        env["values"].append({
            "key": key,
            "value": value,
            "enabled": True
        })

    with open(env_path, "w") as f:
        json.dump(env, f, indent=2)

def load_env(env_path):
    with open(env_path) as f:
        return json.load(f)