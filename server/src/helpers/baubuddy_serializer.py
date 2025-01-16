def calculate_similarity_score(dict1, dict2):
    """
    Compare two dictionaries and return a similarity score based on matching key-value pairs.
    """

    score = 0
    total_keys = 0

    common_keys = dict1.keys() & dict2.keys()

    for key in common_keys:
        total_keys += 1
        if dict1[key] is not None and dict2[key] is not None and dict1[key] == dict2[key]:
            score += 1

    return score / total_keys if total_keys > 0 else 0

def merge_based_on_similarity(api_response, csv_response, threshold=0.5):
    """
    Merge dictionaries from two lists.
    """
    def merge_dicts(dict1, dict2):
        return {key: dict1.get(key) if dict1.get(key) is not None else dict2.get(key) for key in dict1.keys() | dict2.keys()}

    merged = []
    for item1 in api_response:
        for item2 in csv_response:
            score = calculate_similarity_score(item1, item2)
            if score >= threshold:
                merged.append(merge_dicts(item1, item2))
                break
            merged.append(item1)
    return merged


def filter_data_by_column_is_not_none(merged_items, column_name="hu"):
    return [i for i in merged_items if i.get(column_name) is not None and bool(i.get(column_name) and i.get(column_name).strip())]

def setup_colors(merged_items, client):
    for item in merged_items:
        if item.get("labelIds") is not None and bool(item.get("labelIds")):
            label_colors = []
            for label in item.get("labelIds").strip().split(","):
                label_colors.append(client.get_colors(label))
            item["labelIds"] = ','.join(label_colors)
            # "134,133"

    return merged_items