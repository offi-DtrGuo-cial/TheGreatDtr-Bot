# Test code for Hard Points system (hp_folder.hardpoints.py)

# Import modules
from hp_folder.hardpoints import Hard_Points as HP
import asyncio

# Reset file:
with open('hp_folder/hp-list.txt', 'w') as file:
  file.write('USERS = ')

# Asynchronous function for asynchronous tests
async def f():
  # Initialisation
  print(await HP.new('Dtr. Guo'))
  # print('find() returns ' + str('alpha'.find('b')) + ' when a substring isn\'t found')
  print(await HP.points('Twilight', True))
  print(await HP.inc('Discotek'))
  print()

  # Read files
  ## print(await HP.read(''))

  # Accessing
  print(await HP.inc('Discotek'))
  print(await HP.set('Dtr. Guo', 100))
  print(await HP.set('Twilight', 50))
  print(await HP.points('Discotek'))
  print(await HP.points('Twilight', True))
  print(await HP.sat('Dtr. Guo'))
  print()

  # Mutating
  print(await HP.add('Varrick', 30))
  print(await HP.set('Kaiba', 3000))
  print()

  # Reset and deletion
  print(await HP.reset('Discotek'))
  print(await HP.delete('Discotek'))

asyncio.run(f())
