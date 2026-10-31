import unittest

from classes.resource_inventory import ResourceInventory


class ResourceInventoryTests(unittest.TestCase):
    def setUp(self):
        self.inventory = ResourceInventory({
            "wood_log": 64,
            "wood_plank": 64,
        })

    def test_add_and_read_materials(self):
        self.inventory.add("wood_log", 2)
        self.assertEqual(self.inventory.amount("wood_log"), 2)

    def test_rejects_stack_overflow_without_mutating_inventory(self):
        self.inventory.add("wood_plank", 63)
        with self.assertRaises(ValueError):
            self.inventory.add("wood_plank", 2)
        self.assertEqual(self.inventory.amount("wood_plank"), 63)

    def test_consume_many_is_atomic_when_materials_are_missing(self):
        self.inventory.add("wood_plank", 4)
        consumed = self.inventory.consume_many({
            "wood_log": 1,
            "wood_plank": 5,
        })
        self.assertFalse(consumed)
        self.assertEqual(self.inventory.amount("wood_log"), 0)
        self.assertEqual(self.inventory.amount("wood_plank"), 4)

    def test_consume_many_removes_all_required_materials(self):
        self.inventory.add("wood_log", 1)
        self.inventory.add("wood_plank", 5)
        consumed = self.inventory.consume_many({
            "wood_log": 1,
            "wood_plank": 5,
        })
        self.assertTrue(consumed)
        self.assertEqual(self.inventory.snapshot(), {})

    def test_snapshot_cannot_mutate_internal_state(self):
        self.inventory.add("wood_log", 1)
        snapshot = self.inventory.snapshot()
        snapshot["wood_log"] = 99
        self.assertEqual(self.inventory.amount("wood_log"), 1)

    def test_rejects_non_positive_amounts(self):
        with self.assertRaises(ValueError):
            self.inventory.add("wood_log", 0)
        with self.assertRaises(ValueError):
            self.inventory.consume("wood_log", -1)


if __name__ == "__main__":
    unittest.main()
