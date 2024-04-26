import unittest
from your_script_name import extract_age, extract_education_field, extract_work_history

class TestExtractionMethods(unittest.TestCase):
    def test_extract_age(self):
        # Test cases for extract_age function
        self.assertEqual(extract_age("علی 30 ساله"), 30)
        self.assertEqual(extract_age("علی 20 ساله"), 20)
        self.assertIsNone(extract_age("علی 200 ساله"))
        self.assertIsNone(extract_age("علی 5 ساله"))
        self.assertIsNone(extract_age("علی ساله"))
        self.assertIsNone(extract_age(""))

    def test_extract_education_field(self):
        # Test cases for extract_education_field function
        self.assertEqual(extract_education_field("علی مدرک کارشناسی"), ("کارشناسی", None))
        self.assertEqual(extract_education_field("علی مدرک لیسانس"), ("لیسانس", None))
        self.assertEqual(extract_education_field("علی مدرک فوق لیسانس رشته ریاضی"), ("فوق لیسانس", "ریاضی"))
        self.assertEqual(extract_education_field("علی دبیرستان رشته علوم تجربی"), ("دبیرستان", "علوم تجربی"))
        self.assertEqual(extract_education_field(""), (None, None))  # Empty text

    def test_extract_work_history(self):
        # Test cases for extract_work_history function
        self.assertEqual(extract_work_history("علی تجربه کار در حوزه نرم‌افزار"), "حوزه نرم‌افزار")
        self.assertEqual(extract_work_history("علی سابقه کار برنامه‌نویسی دارد"), "برنامه‌نویسی")
        self.assertIsNone(extract_work_history("علی تجربه حوزه نرم‌افزار"))
        self.assertIsNone(extract_work_history(""))

if __name__ == '__main__':
    unittest.main()
