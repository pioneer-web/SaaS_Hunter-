from django.test import SimpleTestCase

from .market import calculate_saturation


class MarketIntelligenceTests(SimpleTestCase):

    def test_low_saturation(self):
        score, level = calculate_saturation(
            competitor_count=2,
            strong_count=0,
            top_stars=100,
        )

        self.assertLess(score, 30)
        self.assertEqual(level, "low")

    def test_high_saturation(self):
        score, level = calculate_saturation(
            competitor_count=20,
            strong_count=5,
            top_stars=15000,
        )

        self.assertGreaterEqual(score, 80)
        self.assertEqual(level, "very_high")

    def test_score_never_above_100(self):
        score, _ = calculate_saturation(
            competitor_count=100,
            strong_count=100,
            top_stars=1000000,
        )

        self.assertEqual(score, 100)
