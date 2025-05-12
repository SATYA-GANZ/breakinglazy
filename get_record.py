from banner import random_art
import rich
from rich.console import Console
import random as r
from datetime import datetime
import time
import csv
from rich.progress import Progress
from rich.table import Table


console = Console()
def get_log():
    console.print(random_art())
    file_exist = input("input a log file : ")
    if file_exist is not None:
     try:
      with open(file_exist, newline = '', encoding='utf-8') as r:
        reader = csv.reader(r)
        header = next(reader)
        rows = list(reader)
        
        total_row = len(rows)
        total_column = len(header)
        
        table = Table(title="Log Record Working Hour")
        for column_name in header:
          table.add_column(column_name, style="cyan", overflow="fold")
        
        for row in rows:
          table.add_row(*row)
     except FileNotFoundError:
        console.print(f"File {file_exist} isn't found, try input a correct file!", style = "bold red")
        return
     except ValueError:
        console.print("empty file!", style = "bold red")
        return
     except UnicodeDecodeError:
        console.print("wrong encoding type, try use utf-8")
        return
      
     console.print(f"current column : {total_column}\ncurrent row    : {total_row}", style="bold green")
      
     console.print(table)