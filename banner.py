import pyfiglet
import random as r

def random_banner():
  font_banner = ["banner3-D", "slant", "3-d", "", "doh", "isometric1"]
  result = pyfiglet.figlet_format("automata", font =  r.choice(font_banner))
  return result

def random_art():
  ascii_art = [
    r"""
        .------.
       / -   -  \
      |  .-. .- |    ____________
      |  | | | | |  |            |
      |  |_| |_| |  |  SECURITY  |
      |  .--. .--|  |  ANALYSIS  |
      | |  | |   |  |   MODULE    |
       \ \_/ \_/ /   |____________|
        '-.___.-'  
       __|     |__  
      /  \     /  \ 
     |    |   |    |
     """""""""""""""
  """""", 
  r"""
       .---------------.
      /   >_<   |  []  \
     |   (o_o)  |  {}   |
     |   /| |\  |  <>   |
     |   / \ \  |  ()   |
      \         |       /
       '--------^------'
           \   /
            \_/
        __/   \__
       |         |
       |_________|
""",

r"""
       .-"      "-.
      /            \
     |              |
     |,  .-.  .-.  ,|   [SYS_CORE]
     | )(_o/  \o_)( |   User: xxxxxxx
     |/     /\     \|   Mode: Stealth
     (_     ^^     _)   Signal: Encrypted
      \__|IIIIII|__/    -------------------
       | \IIIIII/ |     Welcome back...
       \          /
        `--------`
       __||____||__
     /__/-._.--.-_\__\
    [===|=|====|=|===]

"""
  ]
  result =  r.choice(ascii_art)
  return result