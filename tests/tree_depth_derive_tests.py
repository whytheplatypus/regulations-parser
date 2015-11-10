from unittest import TestCase

from regparser.tree.depth import markers, rules
from regparser.tree.depth.derive import derive_depths
from regparser.tree.depth.markers import INLINE_STARS, MARKERLESS, STARS_TAG


class DeriveTests(TestCase):
    def assert_depth_match(self, markers, *depths_set):
        self.assert_depth_match_extra(markers, [], *depths_set)

    def assert_depth_match_extra(self, markers, extra, *depths_set):
        """Verify that the set of markers resolves to the provided set of
        depths (in any order). Allows extra contraints."""
        solutions = derive_depths(markers, extra)
        results = [[a.depth for a in s] for s in solutions]
        self.assertItemsEqual(results, depths_set)

    def test_ints(self):
        self.assert_depth_match(['1', '2', '3', '4'],
                                [0, 0, 0, 0])

    def test_alpha_ints(self):
        self.assert_depth_match(['A', '1', '2', '3'],
                                [0, 1, 1, 1])

    def test_alpha_ints_jump_back(self):
        self.assert_depth_match(['A', '1', '2', '3', 'B', '1', '2', '3', 'C'],
                                [0, 1, 1, 1, 0, 1, 1, 1, 0])

    def test_roman_alpha(self):
        self.assert_depth_match(
            ['a', '1', '2', 'b', '1', '2', '3', '4', 'i', 'ii', 'iii', '5',
             'c', 'd', '1', '2', 'e'],
            [0, 1, 1, 0, 1, 1, 1, 1, 2, 2, 2, 1, 0, 0, 1, 1, 0])

    def test_mix_levels_roman_alpha(self):
        self.assert_depth_match(
            ['A', '1', '2', 'i', 'ii', 'iii', 'iv', 'B', '1', 'a', 'b', '2',
             'a', 'b', 'i', 'ii', 'iii', 'c'],
            [0, 1, 1, 2, 2, 2, 2, 0, 1, 2, 2, 1, 2, 2, 3, 3, 3, 2])

    def test_i_ambiguity(self):
        self.assert_depth_match(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 1])

        self.assert_depth_match(
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        self.assert_depth_match(
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'ii'],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1])

    def test_repeat_alpha(self):
        self.assert_depth_match(
            ['A', '1', 'a', 'i', 'ii', 'a', 'b', 'c', 'b'],
            [0, 1, 2, 3, 3, 4, 4, 4, 2])

    def test_simple_stars(self):
        self.assert_depth_match(['A', '1', STARS_TAG, 'd'],
                                [0, 1, 2, 2])

        self.assert_depth_match(['A', '1', 'a', STARS_TAG, 'd'],
                                [0, 1, 2, 2, 2])

    def test_ambiguous_stars(self):
        self.assert_depth_match(['A', '1', 'a', STARS_TAG, 'B'],
                                [0, 1, 2, 2, 0],
                                [0, 1, 2, 3, 3])

    def test_double_stars(self):
        self.assert_depth_match(['A', '1', 'a', STARS_TAG, STARS_TAG, 'B'],
                                [0, 1, 2, 2, 1, 0],
                                [0, 1, 2, 3, 2, 0],
                                [0, 1, 2, 3, 1, 0])

    def test_alpha_roman_ambiguous(self):
        self.assert_depth_match(['i', 'ii', STARS_TAG, 'v', STARS_TAG, 'vii'],
                                [0, 0, 1, 1, 2, 2],
                                [0, 0, 1, 1, 0, 0],
                                [0, 0, 0, 0, 0, 0])

    def test_start_star(self):
        self.assert_depth_match(
            [STARS_TAG, 'c', '1', STARS_TAG, 'ii', 'iii', '2', 'i', 'ii',
             STARS_TAG, 'v', STARS_TAG, 'vii', 'A'],
            [0, 0, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 3],
            [0, 0, 1, 2, 2, 2, 1, 2, 2, 3, 3, 2, 2, 3],
            [0, 0, 1, 2, 2, 2, 1, 2, 2, 3, 3, 4, 4, 5],
            [0, 0, 1, 2, 2, 2, 1, 2, 2, 0, 0, 1, 1, 2])

    def test_inline_star(self):
        self.assert_depth_match(['1', STARS_TAG, '2'],
                                [0, 1, 0])

        self.assert_depth_match(['1', INLINE_STARS, '2'],
                                [0, 1, 0])

        self.assert_depth_match(['1', INLINE_STARS, 'a'],
                                [0, 1, 1])

    def test_star_star(self):
        self.assert_depth_match(['A', STARS_TAG, STARS_TAG, 'D'],
                                [0, 1, 0, 0])

        self.assert_depth_match(['A', INLINE_STARS, STARS_TAG, '3'],
                                [0, 1, 1, 1])

    def test_markerless_outermost(self):
        """A pattern often seen in definitions sections"""
        self.assert_depth_match(
            [MARKERLESS, MARKERLESS, 'a', 'b', MARKERLESS, 'a', 'b'],
            [0, 0, 1, 1, 0, 1, 1])

    def test_markerless_repeated(self):
        """Repeated markerless paragraphs must be on the same level"""
        self.assert_depth_match(
            [MARKERLESS, 'a', MARKERLESS, MARKERLESS],
            [0, 1, 0, 0],
            [0, 1, 2, 2])

    def test_ii_is_not_ambiguous(self):
        """We've fixed ii to be a roman numeral"""
        self.assert_depth_match(
            ['a', STARS_TAG, 'ii'],
            [0, 1, 1])

    def test_depth_type_order_single(self):
        """Constrain depths to have certain types."""
        extra = rules.depth_type_order([markers.ints, markers.lower])
        self.assert_depth_match_extra(['1', 'a'], [extra], [0, 1])
        self.assert_depth_match_extra(['i', 'a'], [extra])

    def test_depth_type_order_multiple(self):
        """Constrain depths to be in a list of types."""
        extra = rules.depth_type_order([(markers.ints, markers.roman),
                                        markers.lower])
        self.assert_depth_match_extra(['1', 'a'], [extra], [0, 1])
        self.assert_depth_match_extra(['i', 'a'], [extra], [0, 1])

    def test_depth_type_inverses_t2d(self):
        """Two markers of the same type should have the same depth"""
        self.assert_depth_match(
            ['1', STARS_TAG, 'b', STARS_TAG, 'C', STARS_TAG, 'd'],
            [0, 1, 1, 2, 2, 3, 3],
            [0, 1, 1, 2, 2, 1, 1])

        self.assert_depth_match_extra(
            ['1', STARS_TAG, 'b', STARS_TAG, 'C', STARS_TAG, 'd'],
            [rules.depth_type_inverses],
            [0, 1, 1, 2, 2, 1, 1])

    def test_depth_type_inverses_d2t(self):
        """Two markers of the same depth should have the same type"""
        self.assert_depth_match(
            ['1', STARS_TAG, 'c', '2', INLINE_STARS, 'i', STARS_TAG, 'iii'],
            [0, 1, 1, 0, 1, 1, 1, 1],
            [0, 1, 1, 0, 1, 1, 2, 2])

        self.assert_depth_match_extra(
            ['1', STARS_TAG, 'c', '2', INLINE_STARS, 'i', STARS_TAG, 'iii'],
            [rules.depth_type_inverses],
            [0, 1, 1, 0, 1, 1, 2, 2])

    def test_depth_type_inverses_markerless(self):
        """Markerless paragraphs should not trigger an incompatibility"""
        self.assert_depth_match_extra(
            ['1', MARKERLESS, '2', 'a'],
            [rules.depth_type_inverses],
            [0, 1, 0, 1])
