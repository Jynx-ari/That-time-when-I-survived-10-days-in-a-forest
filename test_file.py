import unittest
from classes.round_manager import RoundManager
from classes.game_state import GameState

class TestRoundManager(unittest.TestCase):

    def test_wave_transitions(self):
        rounds = RoundManager()

        self.assertEqual(rounds.day, 1)
        self.assertEqual(rounds.phase, rounds.PREP)

        self.assertTrue (rounds.start_wave())
        self.assertEqual(rounds.phase, rounds.ACTIVE_WAVE)

        self.assertFalse(rounds.start_wave())

        self.assertEqual(rounds.clear_wave(), 30)
        self.assertEqual(rounds.phase, rounds.WAVE_CLEARED)

        self.assertEqual(rounds.clear_wave(),0)


    def test_cannot_advance_before_wave_is_cleared(self):
        rounds = RoundManager()

        self.assertFalse(rounds.advance_day())
        self.assertEqual(rounds.day, 1)

    def test_reach_day_10_without_day_11(self):
        rounds = RoundManager(total_days=10)

        for expected_day in range(1, 11):
            self.assertEqual(rounds.day, expected_day)
            self.assertTrue(rounds.start_wave())
            self.assertEqual(rounds.clear_wave(), 30)

            if expected_day < 10:
                self.assertTrue(rounds.advance_day())
            else:
                self.assertFalse(rounds.advance_day())

        
        self.assertEqual(rounds.day, 10)
        self.assertEqual(rounds.phase, rounds.WAVE_CLEARED)


class TestGameState(unittest.TestCase):
    def test_run_can_onl_end_once(self):
        game = GameState()

        self.assertTrue(game.defeat("Test Defeat"))
        self.assertEqual(game.state, game.DEFEAT)
        
        self.assertFalse(game.win())
        self.assertEqual(game.state, game.DEFEAT)


if __name__ == "__main__":
    unittest.main()