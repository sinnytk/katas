import pprint


def _flatten_list_item(list_item: list, parent_key: str) -> dict:
    dict_from_list = {}
    for idx, value in enumerate(list_item):
        flattened_key = f"{parent_key}_{idx}"
        if type(value) is dict:
            dict_from_list.update(flatten(value, flattened_key))
        elif type(value) is list:
            dict_from_list.update(_flatten_list_item(value, flattened_key))
        else:
            dict_from_list[flattened_key] = value
    return dict_from_list


def flatten(nested_dict: dict, parent_key="") -> dict:
    flattened_dict = {}
    for key, value in nested_dict.items():
        flattened_key = f"{parent_key}.{key}" if parent_key else key
        if type(value) is dict:
            flattened_dict.update(flatten(value, flattened_key))
        elif type(value) is list:
            flattened_dict.update(_flatten_list_item(value, flattened_key))
        else:
            flattened_dict[flattened_key] = value
    return flattened_dict


def main():
    nested_dict = {}
    pprint.pprint(flatten(nested_dict))


if __name__ == "__main__":
    main()
