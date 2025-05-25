import unittest
import re
from Singer import Singer, ConcertOrganizer 

class TestSinger(unittest.TestCase):

    def setUp(self):
        self.valid_performances = [("Budapest Park", "2024-08-10"), ("Akvárium Klub", "2024-09-15")]
        self.singer1 = Singer("Test Singer 1", "Pop", [("Venue A", "Date 1")])
        self.singer2 = Singer("Test Singer 2", "Rock", [("Venue B", "Date 2"), ("Venue C", "Date 3")])
        self.singer_no_perf = Singer("No Show Singer", "Jazz", [])

    def test_singer_init_valid(self):
        name = "Valid Singer"
        genre = "Rock"
        performances = self.valid_performances[:]
        singer = Singer(name, genre, performances)
        self.assertEqual(singer.name, name)
        self.assertEqual(singer.genre, genre)
        self.assertEqual(singer.performances, performances)
        self.assertIsNot(singer._performances, performances)

    def test_singer_init_empty_name_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "Singer name cannot be empty or whitespace."):
            Singer("", "Pop", [])

    def test_singer_init_whitespace_name_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "Singer name cannot be empty or whitespace."):
            Singer("   ", "Pop", [])

    def test_singer_init_non_string_name_raises_type_error(self):
        with self.assertRaisesRegex(TypeError, "Singer name must be a string."):
            Singer(123, "Pop", [])

    def test_singer_init_empty_genre_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "Singer's genre cannot be empty or whitespace."):
            Singer("Test", "", [])

    def test_singer_init_whitespace_genre_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "Singer's genre cannot be empty or whitespace."):
            Singer("Test", "  ", [])

    def test_singer_init_non_string_genre_raises_type_error(self):
        with self.assertRaisesRegex(TypeError, "Singer's genre must be a string."):
            Singer("Test", None, [])

    def test_singer_init_performances_not_list_raises_type_error(self):
        with self.assertRaisesRegex(TypeError, "Performances must be provided as a list."):
            Singer("Test", "Pop", "not a list")

    def test_singer_init_performances_invalid_item_type_raises_type_error(self):
        with self.assertRaisesRegex(TypeError, "Each performance must be a tuple"):
            Singer("Test", "Pop", [("Venue", "Date"), "not a tuple"])

    def test_singer_init_performances_invalid_tuple_length_raises_type_error(self):
        with self.assertRaisesRegex(TypeError, r"Each performance must be a tuple of \(location, date\)"):
            Singer("Test", "Pop", [("Venue", "Date", "Extra")])
        with self.assertRaisesRegex(TypeError, r"Each performance must be a tuple of \(location, date\)"):
            Singer("Test", "Pop", [("Venue",)])

    def test_singer_init_performances_invalid_tuple_content_type_raises_type_error(self):
        with self.assertRaisesRegex(TypeError, "Both location and date.*must be strings"):
            Singer("Test", "Pop", [(123, "Date")])
        with self.assertRaisesRegex(TypeError, "Both location and date.*must be strings"):
            Singer("Test", "Pop", [("Venue", None)])

    def test_singer_init_performances_invalid_tuple_content_value_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "Location and date.*cannot be empty or whitespace"):
            Singer("Test", "Pop", [("", "Date")])
        with self.assertRaisesRegex(ValueError, "Location and date.*cannot be empty or whitespace"):
            Singer("Test", "Pop", [("Venue", "   ")])

    def test_singer_property_getters(self):
        self.assertEqual(self.singer1.name, "Test Singer 1")
        self.assertEqual(self.singer1.genre, "Pop")
        self.assertEqual(self.singer1.performances, [("Venue A", "Date 1")])
        performances_copy = self.singer1.performances
        self.assertIsNot(self.singer1._performances, performances_copy)
        performances_copy.append(("New", "Test"))
        self.assertEqual(len(self.singer1.performances), 1) 

    def test_singer_property_name_setter_valid(self):
        new_name = "Updated Name"
        self.singer1.name = new_name
        self.assertEqual(self.singer1.name, new_name)
        self.assertEqual(self.singer1._name, new_name)

    def test_singer_property_name_setter_invalid(self):
        original_name = self.singer1.name
        with self.assertRaisesRegex(ValueError, "Singer name cannot be empty or whitespace."):
            self.singer1.name = ""
        self.assertEqual(self.singer1.name, original_name)

        with self.assertRaisesRegex(TypeError, "Singer name must be a string."):
            self.singer1.name = 123
        self.assertEqual(self.singer1.name, original_name)

    def test_singer_property_genre_setter_valid(self):
        new_genre = "Updated Genre"
        self.singer1.genre = new_genre
        self.assertEqual(self.singer1.genre, new_genre)
        self.assertEqual(self.singer1._genre, new_genre)

    def test_singer_property_genre_setter_invalid(self):
        original_genre = self.singer1.genre
        with self.assertRaisesRegex(ValueError, "Singer's genre cannot be empty or whitespace."):
            self.singer1.genre = "  "
        self.assertEqual(self.singer1.genre, original_genre)

        with self.assertRaisesRegex(TypeError, "Singer's genre must be a string."):
            self.singer1.genre = None
        self.assertEqual(self.singer1.genre, original_genre)

    def test_singer_str_with_performances(self):
        output = str(self.singer2)
        self.assertIn("Singer: Test Singer 2", output)
        self.assertIn("Genre: Rock", output)
        self.assertIn("Performances:", output)
        self.assertIn("Location: Venue B, Date: Date 2", output)
        self.assertIn("Location: Venue C, Date: Date 3", output)

    def test_singer_str_without_performances(self):
        output = str(self.singer_no_perf)
        self.assertIn("Singer: No Show Singer", output)
        self.assertIn("Genre: Jazz", output)
        self.assertIn("No scheduled performances.", output)

    def test_singer_add_valid_performance(self):
        perf_to_add = ("Venue D", "Date 4")
        original_perf_count = len(self.singer1.performances)
        new_singer = self.singer1 + perf_to_add
        self.assertIsNot(new_singer, self.singer1)
        self.assertEqual(len(self.singer1.performances), original_perf_count)
        self.assertIsInstance(new_singer, Singer)
        self.assertEqual(new_singer.name, self.singer1.name)
        self.assertEqual(len(new_singer.performances), original_perf_count + 1)
        self.assertIn(perf_to_add, new_singer.performances)

    def test_singer_add_invalid_performance_raises_error(self):
        with self.assertRaises(TypeError):
            self.singer1 + "not a tuple"
        with self.assertRaises(ValueError):
            self.singer1 + ("Venue Only",)
        with self.assertRaises(TypeError):
            self.singer1 + (123, "Date")
        with self.assertRaises(ValueError):
             self.singer1 + (" ", "Date")

    def test_singer_sub_existing_performance(self):
        perf_to_remove = ("Venue B", "Date 2")
        original_perf_count = len(self.singer2.performances)
        new_singer = self.singer2 - perf_to_remove
        self.assertIsNot(new_singer, self.singer2)
        self.assertEqual(len(self.singer2.performances), original_perf_count)
        self.assertIsInstance(new_singer, Singer)
        self.assertEqual(new_singer.name, self.singer2.name)
        self.assertEqual(len(new_singer.performances), original_perf_count - 1)
        self.assertNotIn(perf_to_remove, new_singer.performances)
        self.assertIn(("Venue C", "Date 3"), new_singer.performances)

    def test_singer_sub_non_existing_performance_raises_value_error(self):
        perf_non_existent = ("Non Existent Venue", "Date X")
        expected_message = f"Performance {perf_non_existent} not found for singer {self.singer1.name}."
        expected_regex_pattern = re.escape(expected_message)
        with self.assertRaisesRegex(ValueError, expected_regex_pattern):
            self.singer1 - perf_non_existent

    def test_singer_sub_invalid_performance_raises_error(self):
        with self.assertRaises(TypeError):
            self.singer1 - ["list"]
        with self.assertRaises(ValueError):
            self.singer1 - ("Too", "Many", "Items")

    def test_singer_lt_gt_comparison(self):
        self.assertTrue(self.singer1 < self.singer2)
        self.assertFalse(self.singer2 < self.singer1)
        self.assertTrue(self.singer2 > self.singer1)
        self.assertFalse(self.singer1 > self.singer2)
        self.assertFalse(self.singer1 < self.singer1)
        self.assertFalse(self.singer1 > self.singer1)

    def test_singer_comparison_with_non_singer(self):
        self.assertEqual(self.singer1.__lt__(5), NotImplemented)
        self.assertEqual(self.singer1.__gt__("string"), NotImplemented)

class TestConcertOrganizer(unittest.TestCase):

    def setUp(self):
        self.singer_pop = Singer("Pop Star", "Pop", [("Venue P1", "Date P1"), ("Venue P2", "Date P2")])
        self.singer_rock = Singer("Rock Legend", "Rock", [("Venue R1", "Date R1")])
        self.singer_jazz = Singer("Jazz Master", "Jazz", [("Venue J1", "Date J1"), ("Venue J2", "Date J2")])
        self.singer_folk = Singer("Folk Singer", "Folk", [("Venue F1", "Date F1"), ("Venue F2", "Date F2"), ("Venue F3", "Date F3")])

    def test_organizer_init_empty(self):
        organizer = ConcertOrganizer()
        self.assertEqual(organizer.singers, [])
        self.assertEqual(organizer._singers, [])

    def test_organizer_init_with_valid_list(self):
        singer_list = [self.singer_pop, self.singer_rock]
        organizer = ConcertOrganizer(singer_list)
        self.assertEqual(len(organizer.singers), 2)
        self.assertIn(self.singer_pop, organizer.singers)
        self.assertIn(self.singer_rock, organizer.singers)
        self.assertIsNot(organizer._singers, singer_list)

    def test_organizer_init_with_invalid_list_type_raises_type_error(self):
        with self.assertRaisesRegex(TypeError, "Initial singers must be provided as a list."):
            ConcertOrganizer("not a list")

    def test_organizer_init_with_list_containing_non_singer_raises_type_error(self):
        invalid_list = [self.singer_pop, "not a singer"]
        with self.assertRaisesRegex(TypeError, "All elements in the initial list must be Singer instances."):
            ConcertOrganizer(invalid_list)

    def test_organizer_property_singers_getter(self):
        singer_list = [self.singer_pop]
        organizer = ConcertOrganizer(singer_list)
        singers_copy = organizer.singers
        self.assertEqual(singers_copy, singer_list)
        self.assertIsNot(singers_copy, organizer._singers)
        singers_copy.append(self.singer_rock)
        self.assertEqual(len(organizer.singers), 1)

    def test_organizer_add_singer_valid(self):
        organizer = ConcertOrganizer()
        organizer.add_singer(self.singer_pop)
        self.assertEqual(len(organizer.singers), 1)
        self.assertIn(self.singer_pop, organizer.singers)

    def test_organizer_add_singer_duplicate(self):
        organizer = ConcertOrganizer([self.singer_pop])
        organizer.add_singer(self.singer_pop)
        self.assertEqual(len(organizer.singers), 1)

    def test_organizer_add_singer_invalid_type_raises_type_error(self):
        organizer = ConcertOrganizer()
        with self.assertRaisesRegex(TypeError, "Only Singer objects can be added."):
            organizer.add_singer("not a singer")

    def test_organizer_str_empty(self):
        organizer = ConcertOrganizer()
        self.assertEqual(str(organizer), "Concert Organizer (No singers registered)")

    def test_organizer_str_with_singers(self):
        organizer = ConcertOrganizer([self.singer_pop, self.singer_rock])
        output = str(organizer)
        self.assertIn("Concert Organizer (2 singers registered)", output)
        self.assertIn(self.singer_pop.name, output)
        self.assertIn(self.singer_rock.name, output)

    def test_find_most_performances_empty_raises_value_error(self):
        organizer = ConcertOrganizer()
        with self.assertRaisesRegex(ValueError, "No singers registered"):
            organizer.find_singers_with_most_performances()

    def test_find_most_performances_one_singer(self):
        organizer = ConcertOrganizer([self.singer_rock])
        result = organizer.find_singers_with_most_performances()
        self.assertEqual(result, [self.singer_rock])

    def test_find_most_performances_clear_winner(self):
        organizer = ConcertOrganizer([self.singer_pop, self.singer_rock, self.singer_folk])
        result = organizer.find_singers_with_most_performances()
        self.assertEqual(result, [self.singer_folk])

    def test_find_most_performances_tie(self):
        organizer = ConcertOrganizer([self.singer_pop, self.singer_rock, self.singer_jazz])
        result = organizer.find_singers_with_most_performances()
        self.assertEqual(len(result), 2)
        self.assertIn(self.singer_pop, result)
        self.assertIn(self.singer_jazz, result)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
