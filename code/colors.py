from enum import Enum

class Colors(Enum):
     """
     This Enumeration collects some well chosen ansi escape sequences for graphic rendition
     parameters using control sequence introducer commands to generate colored output in console,
     like described in: https://en.wikipedia.org/wiki/ANSI_escape_code
     """

     WHITE = "\033[97m"
     CYAN = "\033[96m"
     PURPLE = "\033[95m"
     BLUE = "\033[94m"
     YELLOW = "\033[93m"
     GREEN = "\033[92m"
     RED = "\033[91m"
     GREY = "\033[90m"
     CROSSED = "\033[9m"
     INVERTED = "\033[7m"
     BLINKING = "\033[5m"
     UNDERLINE = "\033[4m"
     ITALIC = "\033[3m"
     BOLD = "\033[1m"
     END = "\033[0m"

     def to_err_str(text:str) -> str:
          return Colors.to_str(text,Colors.RED)
     
     def to_may_str(text:str) -> str:
          return Colors.to_str(text,Colors.YELLOW)
     
     def to_right_str(text:str) -> str:
          return Colors.to_str(text,Colors.GREEN)

     def to_str(text:str,color) -> str:
          return color.value + text + Colors.END.value