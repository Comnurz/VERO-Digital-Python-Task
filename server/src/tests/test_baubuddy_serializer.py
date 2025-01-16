import unittest
from unittest.mock import patch, Mock
from helpers.baubuddy_serializer import (filter_data_by_column_is_not_none,
                                         setup_colors, merge_based_on_similarity, calculate_similarity_score)

class TestBaubuddySerializer(unittest.TestCase):
    def test_filter_data_by_column_is_not_none(self):
        items = [
            {"hu": "value1", "other": "data1"},
            {"hu": "value2", "other": "data2"},
            {"hu": None, "other": "data3"},
            {"hu": " ", "other": "data4"},
            {"hu": "", "other": "data5"}
        ]
        expected_result = [
            {"hu": "value1", "other": "data1"},
            {"hu": "value2", "other": "data2"}
        ]
        result = filter_data_by_column_is_not_none(items)
        self.assertEqual(expected_result, result)

    def test_filter_data_by_column_name_is_not_none_with_different_column(self):
        items = [
            {"hu": "value1", "other": "data1"},
            {"hu": "value2", "other": "data2"},
            {"hu": None, "other": "data3"},
            {"hu": " ", "other": "data4"},
            {"hu": "", "other": "data5"}
        ]
        result = filter_data_by_column_is_not_none(items, "other")
        self.assertEqual(result, result)

    def test_filter_data_by_column_name_is_not_none_with_empty_list(self):
        items = []
        result = filter_data_by_column_is_not_none(items)
        self.assertEqual([], result)

    def test_filter_data_with_no_matching_column(self):
        data = [
            {"hu": "value1", "other": "data1"},
            {"hu": "value2", "other": "data2"}
        ]
        result = filter_data_by_column_is_not_none(data, "nonexistent")
        self.assertEqual([], result)

    def test_setup_colors_with_valid_label_ids(self):
        client = Mock()
        client.get_colors.side_effect = lambda label: f"color_{label}"
        merged_list = [{"labelIds": "1,2,3"}]
        result = setup_colors(merged_list, client)
        self.assertEqual([{"labelIds": "color_1,color_2,color_3"}], result)

    def test_setup_colors_with_empty_label_ids(self):
        client = Mock()
        merged_items = [{"labelIds": ""}]
        result = setup_colors(merged_items, client)
        self.assertEqual([{"labelIds": ""}], result)

    def test_setup_colors_with_none_label_ids(self):
        client = Mock()
        merged_items = [{"labelIds": None}]
        result = setup_colors(merged_items, client)
        self.assertEqual([{"labelIds": None}], result)

    def test_setup_colors_with_mixed_label_ids(self):
        client = Mock()
        client.get_colors.side_effect = lambda label: f"color_{label}"
        merged_items = [{"labelIds": "1,2,3"}, {"labelIds": None}, {"labelIds": ""}, {"labelIds": ''}]
        expected_result = [
            {"labelIds": "color_1,color_2,color_3"},
            {"labelIds": None},
            {"labelIds": ""},
            {"labelIds": ""}
        ]
        result = setup_colors(merged_items, client)
        self.assertEqual(expected_result, result)

    @patch("helpers.baubuddy_serializer.calculate_similarity_score")
    def test_merge_based_on_similarity_first_has_none(self, calculate_similarity_score_mock):
        calculate_similarity_score_mock.return_value = 0.5
        list1 = [{"a": 1, "b": None, "c": 3}]
        list2 = [{"a": 1, "b": 2}]
        result = merge_based_on_similarity(list1, list2)
        self.assertEqual([{"a": 1, "b": 2, "c": 3}], result)

    @patch("helpers.baubuddy_serializer.calculate_similarity_score")
    def test_merge_based_on_similarity_not_similar(self, calculate_similarity_score_mock):
        calculate_similarity_score_mock.return_value = 0.4
        list1 = [{"a": 1, "b": None}]
        list2 = [{"a": 1, "b": 2}]
        result = merge_based_on_similarity(list1, list2)
        self.assertEqual([{"a": 1, "b": None}], result)

    @patch("helpers.baubuddy_serializer.calculate_similarity_score")
    def test_merge_based_on_similarity_second_list_has_none(self, calculate_similarity_score_mock):
        calculate_similarity_score_mock.return_value = 0.5
        list1 = [{"a": 1, "b": 2}]
        list2 = [{"a": 1, "b": None, "c": 3}]
        result = merge_based_on_similarity(list1, list2)
        self.assertEqual([{"a": 1, "b": 2, "c": 3}], result)

    @patch("helpers.baubuddy_serializer.calculate_similarity_score")
    def test_merge_based_on_similarity_len_of_lists_equal(self, calculate_similarity_score_mock):
        calculate_similarity_score_mock.return_value = 0.5
        list1 = [{"a": 1, "b": 2}]
        list2 = [{"a": 1, "b": None}]
        result = merge_based_on_similarity(list1, list2)
        result_2 = merge_based_on_similarity(list2, list1)
        self.assertEqual([{"a": 1, "b": 2}], result)
        self.assertEqual([{"a": 1, "b": 2}], result_2)

    def test_calculate_similarity_score(self):
        list1 = {"a": 1, "b": 2}
        list2 = {"a": 1, "b": None}
        result = calculate_similarity_score(list1, list2)
        self.assertEqual(0.5, result)

    def test_calculate_similarity_score_with_no_similar_values(self):
        list1 = {"a": 3, "b": 2}
        list2 = {"a": 1, "b": None}
        result = calculate_similarity_score(list1, list2)
        self.assertEqual(0.0, result)

    def test_calculate_similarity_score_with_two_similar_values(self):
        list1 = {"a": 1, "b": 2, 'c': 4}
        list2 = {"a": 1, "b": 2, 'c': None}
        result = calculate_similarity_score(list1, list2)
        self.assertEqual(2/3, result)

    def test_calculate_similarity_score_with_similar_values(self):
        list1 = {"a": 1, "b": None, 'c': 4}
        list2 = {"a": 1, "b": None, 'c': None}
        result = calculate_similarity_score(list1, list2)
        self.assertEqual(1/3, result)

    def test_calculate_similarity_score_with_identical_dicts(self):
        list1 = {"a": 1, "b": 2, 'c': 4}
        list2 = {"a": 1, "b": 2, 'c': 4}
        result = calculate_similarity_score(list1, list2)
        self.assertEqual(1.0, result)

    def test_calculate_similarity_score_with_empty_dicts(self):
        list1 = {}
        list2 = {}
        result = calculate_similarity_score(list1, list2)
        self.assertEqual(0.0, result)

