""" Unpack a dictionary showing its hierarchy & low level values."""


def print_dict_hierarchy(self, data, parent_keys=None):
    """Recursively prints key-value pairs with their hierarchical path.

    Args:
        data (dict): The dictionary to traverse.
        parent_keys (list, optional): A list of parent keys. Defaults to None.
    """
    if parent_keys is None:
        parent_keys = []
    for key, value in data.items():
        current_path = " -> ".join(parent_keys + [key])
        if isinstance(value, dict):
            self.print_dict_hierarchy(value, parent_keys + [key])
        elif isinstance(value, list):
            for i, item in enumerate(value):
                list_key = f"[{i}]"  # Represent list index as a key
                print(f"{' -> '.join(parent_keys + [key, list_key])} ---> {item}")
        else:
            print(f"{current_path} ---> {value}")

