from GUI import SOSGame
import tkinter as tk
from UnitTests import unittest

if __name__ == "__main__":
    window = tk.Tk()
    game = SOSGame(window)
    window.mainloop()
    unittest.main()