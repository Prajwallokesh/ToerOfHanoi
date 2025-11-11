class HanoiSolver:
    def __init__(self, game_logic):
        self.game = game_logic

    def solve(self, n, from_peg=0, to_peg=2, helper_peg=1):
        """Solve Tower of Hanoi recursively, returning list of moves"""
        if n == 1:
            return [(from_peg, to_peg)]
        else:
            moves = []
            # Move n-1 disks from source to helper using destination as helper
            moves.extend(self.solve(n-1, from_peg, helper_peg, to_peg))
            # Move the nth disk from source to destination
            moves.append((from_peg, to_peg))
            # Move n-1 disks from helper to destination using source as helper
            moves.extend(self.solve(n-1, helper_peg, to_peg, from_peg))
            return moves

    def get_solution_moves(self, num_disks):
        """Get the complete list of moves to solve the puzzle"""
        return self.solve(num_disks)

    def get_remaining_moves(self):
        """Get moves to solve from current game state using Tower of Hanoi rules"""
        # For now, just return the full solution from the beginning
        # This assumes the game starts from the initial state
        total_disks = sum(len(peg) for peg in self.game.pegs)
        return self.solve(total_disks)

