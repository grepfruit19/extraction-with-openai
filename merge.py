import unittest

# Merge two dictionaries, replacing any None values.
# If both dictionaries have the same keys, prefer values from dict1
def merge_dicts(dict1, dict2):
    dict1_copy = dict1.copy()  # Create a copy of the first dictionary

    for key, value in dict1.items():
      if value is None:
        if key in dict2:
          # Sometimes the model returns 'null' as a string, we want to ignore that.
          if dict2[key] == 'null':
            continue
          dict1_copy[key] = dict2[key]
    
    return dict1_copy

class TestMerge(unittest.TestCase):
  def test_simple_merge(self):
    dict1 = { "test": "hi", "test2": None, "test3": None }
    dict2 = { "test": None }
    res = merge_dicts(dict1, dict2)
    self.assertDictEqual(res, dict1)

  def test_simple_merge_2(self):
    dict1 = { "test": None }
    dict2 = { "test": "hi" }
    res = merge_dicts(dict1, dict2)
    self.assertDictEqual(res, dict2)

  def test_prefer_dict1(self):
    dict1 = { "test": "hi" }
    dict2 = { "test": "hi2" }
    res = merge_dicts(dict1, dict2)
    self.assertDictEqual(res, dict1)

  def test_dict1_none(self):
    dict1 = { "test": None }
    dict2 = { "test": "hi2" }
    res = merge_dicts(dict1, dict2)
    self.assertDictEqual(res, dict2)

  def test_skip_string_null(self):
    dict1 = { "test": "hi" }
    dict2 = { "test": 'null' }
    res = merge_dicts(dict1, dict2)
    self.assertDictEqual(res, dict1)

# unittest.main()
