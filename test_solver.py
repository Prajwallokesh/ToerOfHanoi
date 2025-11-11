#!/usr/bin/env python3

from game_logic import GameLogic
from hanoi_solver import HanoiSolver

def test_solver():
    # Test with 3 disks
    game = GameLogic()
    game.initialize(3)
    solver = HanoiSolver(game)

    print("Initial state (largest to smallest, bottom to top):")
    print(f"Peg 0: {game.pegs[0]}")
    print(f"Peg 1: {game.pegs[1]}")
    print(f"Peg 2: {game.pegs[2]}")

    moves = solver.get_solution_moves(3)
    print(f"\nSolution moves ({len(moves)} total):")
    for i, (from_peg, to_peg) in enumerate(moves, 1):
        print(f"Move {i}: {from_peg} -> {to_peg}")

    # Execute the moves
    move_count = 0
    for from_peg, to_peg in moves:
        if game.move_disk(from_peg, to_peg):
            move_count += 1
            print(f"After move {move_count}:")
            print(f"Peg 0: {game.pegs[0]}")
            print(f"Peg 1: {game.pegs[1]}")
            print(f"Peg 2: {game.pegs[2]}")
        else:
            print(f"Invalid move: {from_peg} -> {to_peg}")
            break

    print(f"\nFinal state after {move_count} moves:")
    print(f"Peg 0: {game.pegs[0]}")
    print(f"Peg 1: {game.pegs[1]}")
    print(f"Peg 2: {game.pegs[2]}")
    print(f"Is solved: {game.is_solved()}")
    print(f"Expected moves: {(2**3) - 1} = 7")

if __name__ == "__main__":
    test_solver()