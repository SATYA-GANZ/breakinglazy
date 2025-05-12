from banner import random_art
import rich
from rich.console import Console
import random as r
from datetime import datetime
import time
import csv
from rich.progress import Progress
import os

console = Console()
def work_time():
  while True:
    console.print(random_art())
    console.print("ready to work? : ", style = "bold cyan")
    maybe = input("y/n? : ")
    
    if maybe == "y":
     now = datetime.now()
     console.print("current time : ", time.strftime('%H:%M:%S'), style="cyan")
     until = input("input the end of your work (hour) : ")
     agenda = input("input agenda (activity) : ")
    
     if until > now.strftime("%H:%M:%S") and agenda:
       try:
        until_work = datetime.strptime(until, "%H:%M").replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
       except ValueError:
         console.print("wrong format! gunakan HH:MM", style = "bold red")
      
       with Progress() as progress:
           task = progress.add_task("Working....", total = (until_work - datetime.now()).seconds)
           while datetime.now() < until_work:
             progress.update(task, advance=1)
             time.sleep(1)
       console.print("your work has been done at this session!", style="bold cyan")
       reportQuestion = input("name file for save : ")
       
       if reportQuestion != None:
        report_data = [now.strftime("%Y:%m:%d"), now.strftime("%H:%M:%S"), agenda]
       
        file_exist = os.path.exists(reportQuestion)
        with open(reportQuestion, 'a', newline='') as file:
         writer = csv.writer(file)
         
         if not file_exist:
           writer.writerow(["tanggal", "waktu", "agenda"])
         
         writer.writerow(report_data)
         
       console.print("data has been saved!", style="green")
    
    elif maybe == "n":
      console.print("bye!")
      break
   # while maybe not in["y","n"]:
   #   console.print("hanya y/n saja")
    #  maybe = input("y/n : ")
  #    if maybe == "n":
    #    break 