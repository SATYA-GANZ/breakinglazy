import rich
import pyfiglet
import random
from banner import random_banner
from rich.console import Console
import os
from work import work_time
from analisis import main_menu
from get_record import get_log

console = Console()
def menu():
  os.system('cls||clear')
  while True:
   console.print(random_banner(), style="bold red")
   console.print("welcome to main menu", style="bold red")
   console.print("pilih salah satu :", style="bold cyan")
   console.print("""
   1. Start a Ambisious work
   2. Get a record (csv/excel)
   3. analysis data with machine learning
   0. exit
   """)
   option = input("1-3 : ")
   
   match(option):
     case "1":
       work_time()
     case "2":
       get_log()
     case "3":
       main_menu()
     case 0:
       exit()

if __name__ == "__main__":
  menu()