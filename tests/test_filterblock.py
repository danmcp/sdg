# Standard
from unittest.mock import patch
import operator
import unittest

# Third Party
from datasets import Dataset, Features, Value

# First Party
from instructlab.sdg.filterblock import FilterByValueBlock


class TestFilterByValueBlock(unittest.TestCase):
    def setUp(self):
        self.block = FilterByValueBlock(
            filter_column="age",
            filter_value=30,
            operation=operator.eq,
            convert_dtype=int,
        )
        self.dataset = Dataset.from_dict(
            {"age": ["25", "30", "35", "forty", "45"]},
            features=Features({"age": Value("string")}),
        )

    @patch("instructlab.sdg.filterblock.logger")
    def test_generate_mixed_types(self, mock_logger):
        filtered_dataset = self.block.generate(self.dataset)
        self.assertEqual(len(filtered_dataset), 1)
        self.assertEqual(filtered_dataset["age"], [30])
        mock_logger.error.assert_called()
