from Project.config import white
import pygame


class MonetarySystem:
    def __init__(self, initial_balance = 0):
        """
        Monetary System starts with 0 (starting balance).

        Args:
            initial_balance(int):Starting amount of money of the player.
        """
        self.balance = initial_balance


    def money_earned(self, amount):
        """
        Amount of money added to the player´s balance.

        Args:
            amount(int): The amount of money earned
        """
        self.balance += amount

    def spend_money(self, amount):
        """
        Amount of money the player spent.

        Args:
            amount(int): Money to spend
        Return:
            Bool: True if the amount of money spent was less or equal to the balanvce, False otherwise
        """
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def check_balance(self):
        """
        Checks the current balance.
        Returns:
            int: The player´s current balance
        """
        return self.balance

    def show_balance(self, screen, font, x = 10, y = 10): #The coordinates (x=10,y=10) means the text will take place in the upper left corner
        """
        Show´s the amount of money the player has in screen.

        Args:
            screen: Game screen
            font: font
            x(int): Coordinate x to show the balance
            y(int): Coordinate y to show the balance
        """
        creepster_font = pygame.font.Font("assets/Creepster-Regular.ttf", 20)
        text_balance = creepster_font.render(f"Coins: {self.balance} ", True, white)
        screen.blit(text_balance,(x,y))