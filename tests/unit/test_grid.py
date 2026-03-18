"""Unit tests for Grid domain class — Phase 3."""
import pytest
from app.domain.grid import Grid


class TestIsValid:
    """is_valid returns True only for in-bounds, obstacle-free coordinates."""

    def test_origin_is_valid(self):
        g = Grid(10, 10)
        assert g.is_valid(0, 0) is True

    def test_max_corner_is_valid(self):
        g = Grid(10, 10)
        assert g.is_valid(9, 9) is True

    def test_negative_x_is_invalid(self):
        g = Grid(10, 10)
        assert g.is_valid(-1, 0) is False

    def test_negative_y_is_invalid(self):
        g = Grid(10, 10)
        assert g.is_valid(0, -1) is False

    def test_x_equals_width_is_invalid(self):
        g = Grid(10, 10)
        assert g.is_valid(10, 0) is False

    def test_y_equals_height_is_invalid(self):
        g = Grid(10, 10)
        assert g.is_valid(0, 10) is False

    def test_obstacle_position_is_invalid(self):
        g = Grid(10, 10, obstacles=[(5, 5)])
        assert g.is_valid(5, 5) is False

    def test_adjacent_to_obstacle_is_valid(self):
        g = Grid(10, 10, obstacles=[(5, 5)])
        assert g.is_valid(5, 6) is True


class TestHasObstacle:
    """has_obstacle distinguishes obstacle cells from empty ones."""

    def test_obstacle_present(self):
        g = Grid(10, 10, obstacles=[(5, 5)])
        assert g.has_obstacle(5, 5) is True

    def test_no_obstacle_at_adjacent(self):
        g = Grid(10, 10, obstacles=[(5, 5)])
        assert g.has_obstacle(5, 6) is False

    def test_no_obstacles_at_all(self):
        g = Grid(10, 10)
        assert g.has_obstacle(0, 0) is False


class TestBlockReason:
    """is_boundary_block and is_obstacle_block distinguish block causes."""

    def test_out_of_bounds_is_boundary_block(self):
        g = Grid(10, 10)
        assert g.is_boundary_block(10, 0) is True

    def test_obstacle_is_not_boundary_block(self):
        g = Grid(10, 10, obstacles=[(5, 5)])
        assert g.is_boundary_block(5, 5) is False

    def test_obstacle_is_obstacle_block(self):
        g = Grid(10, 10, obstacles=[(5, 5)])
        assert g.is_obstacle_block(5, 5) is True

    def test_out_of_bounds_is_not_obstacle_block(self):
        g = Grid(10, 10)
        assert g.is_obstacle_block(10, 0) is False

    def test_valid_cell_is_neither_block(self):
        g = Grid(10, 10)
        assert g.is_boundary_block(3, 3) is False
        assert g.is_obstacle_block(3, 3) is False
