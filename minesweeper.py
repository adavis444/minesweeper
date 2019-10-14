#!/usr/bin/env python3

from random import randint
from typing import List, Optional


class Minesweeper:
    def __init__(self, height: int = 10, width: int = 10,
                 mines: int = 10) -> None:
        self.height: int = height
        self.width: int = width
        self.mine_count: int = mines
        self.in_progress: bool = True
        self.new_game()

    def new_game(self) -> None:
        # TODO: Use seed value
        self.mines: List[List[bool]] = [[False for j in range(self.width)]
                                        for i in range(self.height)]
        cur_mines: int = 0
        while cur_mines < self.mine_count:
            row: int = randint(0, self.height-1)
            col: int = randint(0, self.width-1)
            if not self.mines[row][col]:
                self.mines[row][col] = True
                cur_mines += 1
        self.remaining: int = self.height*self.width - self.mine_count
        self.visible: List[List[Optional[str]]] = [
            [None for j in range(self.width)] for i in range(self.height)]

    def show(self) -> None:
        for i in range(self.height):
            # TODO: Clean this:
            print(*['.' if x is None else x for x in self.visible[i]])

    def reveal_all(self) -> None:
        for i in range(self.height):
            # TODO: Clean this:
            print(*[['.', 'X'][self.mines[i][j]] if x is None else x for j, x
                    in enumerate(self.visible[i])])

    def click(self, row: int, col: int) -> None:
        if self.visible[row][col]:
            raise ValueError
        if self.mines[row][col]:
            self.visible[row][col] = 'X'
            self.game_over(victory=False)
        else:
            neighboring_mines: int = 0
            for i in (row-1, row, row+1):
                if 0 <= i < self.height:
                    for j in (col-1, col, col+1):
                        if 0 <= j < self.width and self.mines[i][j]:
                            neighboring_mines += 1
            self.visible[row][col] = str(neighboring_mines)
            self.remaining -= 1
            if neighboring_mines == 0:
                for i in (row-1, row, row+1):
                    if 0 <= i < self.height:
                        for j in (col-1, col, col+1):
                            if 0 <= j < self.width and not self.visible[i][j]:
                                self.click(i, j)
        if self.remaining == 0:
            self.game_over(victory=True)

    def flag(self, row: int, col: int) -> None:
        if self.visible[row][col]:
            raise ValueError
        self.visible[row][col] = 'F'

    def unflag(self, row: int, col: int) -> None:
        if self.visible[row][col] != 'F':
            raise ValueError
        self.visible[row][col] = None

    def toggle_flag(self, row: int, col: int) -> None:
        if self.visible[row][col] == 'F':
            self.unflag(row, col)
        elif self.visible[row][col]:
            raise ValueError
        else:
            self.flag(row, col)

    def game_over(self, victory: bool) -> None:
        self.reveal_all()
        if victory:
            print('You won!')
        else:
            print('You lost.')
        self.in_progress = False

    def input_loop(self) -> None:
        while self.in_progress:
            self.show()
            user_input: List[str] = input(
                'Enter the row and column as space-separated '
                '1-indexed integers: '
            ).split()
            try:
                row: int = int(user_input[0]) - 1
                col: int = int(user_input[1]) - 1
                if not 0 <= row < self.height or not 0 <= col < self.width:
                    raise ValueError
                if user_input[2:]:
                    self.toggle_flag(row, col)
                else:
                    self.click(row, col)
            except (ValueError, IndexError):
                continue


if __name__ == '__main__':
    Minesweeper().input_loop()
