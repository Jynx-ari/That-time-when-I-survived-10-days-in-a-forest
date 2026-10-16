import unittest
from classes.round_manager import RoundManager, RoundPhase
from classes.game_state import GameState

class TestRoundManager(unittest.TestCase):

    def test_wave_transitions(self):
        rounds = RoundManager()

        self.assertEqual(rounds.day, 1)
        self.assertEqual(rounds.phase, RoundPhase.PREP)

        self.assertTrue (rounds.start_wave())
        self.assertEqual(rounds.phase, RoundPhase.ACTIVE_WAVE)

        self.assertFalse(rounds.start_wave())

        self.assertEqual(rounds.clear_wave(), True)
        self.assertEqual(rounds.phase, RoundPhase.WAVE_CLEARED)

        self.assertFalse(rounds.clear_wave())


    def test_cannot_advance_before_wave_is_cleared(self):
        rounds = RoundManager()

        self.assertFalse(rounds.advance_day())
        self.assertEqual(rounds.day, 1)

    def test_reach_day_10_without_day_11(self):
        rounds = RoundManager(total_days=10)

        for expected_day in range(1, 11):
            self.assertEqual(rounds.day, expected_day)
            self.assertTrue(rounds.start_wave())
            self.assertEqual(rounds.clear_wave(), True)

            if expected_day < 10:
                self.assertTrue(rounds.advance_day())
            else:
                self.assertTrue(rounds.advance_day())
                self.assertEqual(rounds.phase, RoundPhase.VICTORY)

        
        self.assertEqual(rounds.day, 10)
        self.assertEqual(rounds.phase, RoundPhase.VICTORY)

    def test_victory_cannot_become_defeat(self):
        rounds = RoundManager(total_days=1)
        rounds.start_wave()
        rounds.clear_wave()
        rounds.advance_day()

        self.assertEqual(rounds.phase, RoundPhase.VICTORY)
        self.assertFalse(rounds.end_game())
        self.assertEqual(rounds.phase, RoundPhase.VICTORY)

class TestGameState(unittest.TestCase):
    def test_run_can_onl_end_once(self):
        game = GameState()

        self.assertTrue(game.defeat("Test Defeat"))
        self.assertEqual(game.state, game.DEFEAT)
        
        self.assertFalse(game.win())
        self.assertEqual(game.state, game.DEFEAT)


if __name__ == "__main__":
    unittest.main()