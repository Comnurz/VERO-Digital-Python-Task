from helpers.baubuddyClient import get_colors

def calculate_similarity_score(dict1, dict2):
    """
    Compare two dictionaries and return a similarity score based on matching key-value pairs.
    """
    score = 0
    total_keys = 0

    # Find common keys
    common_keys = dict1.keys() & dict2.keys()

    for key in common_keys:
        total_keys += 1
        if dict1[key] is not None and dict2[key] is not None and dict1[key] == dict2[key]:
            score += 1

    # Avoid division by zero
    return score / total_keys if total_keys > 0 else 0


def merge_based_on_similarity(list1, list2, threshold=0.5):
    """
    Merge dictionaries from two lists if their similarity score exceeds the threshold.
    """
    merged = []
    for item1 in list1:
        for item2 in list2:
            score = calculate_similarity_score(item1, item2)
            if score >= threshold:
                merged.append({**item1, **item2})
    return merged


def filter_data_by_column_is_not_none(merged_items, column_name="hu"):
    return [i for i in merged_items if i.get(column_name) is not None and bool(i.get(column_name) and i.get(column_name).strip())]

def setup_colors(merged_items):
    for item in merged_items:
        if item.get("labelIds") is not None and bool(item.get("labelIds") and item.get("labelIds").strip()):
            item["labelIds"] = get_colors(item.get("labelIds"))
        else:
            item["labelIds"] = "FFFFFF"

    return merged_items