class GameLogic:
    def __init__(self):
        self.pegs = []  # List of lists, each sublist is disks on that peg, top is last

    def initialize(self, num_disks):
        self.pegs = [list(range(num_disks-1, -1, -1)), [], []]  # Largest disk at bottom

    def move_disk(self, from_peg, to_peg):
        if not self.pegs[from_peg]:
            return False  # No disk to move
        disk = self.pegs[from_peg][-1]
        if self.pegs[to_peg] and self.pegs[to_peg][-1] < disk:
            return False  # Cannot place larger on smaller
        self.pegs[from_peg].pop()
        self.pegs[to_peg].append(disk)
        return True

    def is_solved(self):
        return len(self.pegs[2]) == len(self.pegs[0]) + len(self.pegs[1]) + len(self.pegs[2]) and not self.pegs[0] and not self.pegs[1]