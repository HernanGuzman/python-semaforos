import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
semaphorePlatos = threading.Semaphore(3)
semaphoreCocinero = threading.Semaphore(1)
platosTotales  = 3
platosDisponibles = 3
class Cocinero(threading.Thread):
  def __init__(self):
    super().__init__()
    self.name = 'Cocinero'

  def run(self):
    #Cuando llaman al cocinero se preparan los platos hasta llegar a la cantidad
    #de platos y vuelvo a hacer dormir al cocinero
    global platosDisponibles
    logging.info('Reponiendo los platos...')
    while (platosDisponibles< platosTotales):
      platosDisponibles += 1
      semaphorePlatos.release()
    semaphoreCocinero.release()  


class Comensal(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = f'Comensal {numero}'

  def run(self):
    global platosDisponibles
    #Para no despertar muchas veces al cocinero, cuando un comensal quiere comer y no hay platos
    #llamo al cocinero para que prepare los platos
    semaphoreCocinero.acquire()
    if platosDisponibles == 0:
      Cocinero().start()
    semaphorePlatos.acquire()
    platosDisponibles -= 1
    logging.info(f'¡Qué rico! Quedan {platosDisponibles} platos')
    semaphoreCocinero.release()  
    
      
    


for i in range(5):
  Comensal(i).start()

