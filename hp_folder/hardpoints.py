# Modules import
import asyncio

''' Hard_Points struct:
{
  NAME = Discord application username (not nick)
  HP = Hard Points, init zero
  SAT = Saturation level, init 'unsaturated'
}

Compacted using newlines and tabs
'''

# Static class
class Hard_Points:
  # Instantiable local class
  class hp_struct:
    ''' Hard_Points.hp_struct
    Local class of Hard_Points to organise and abstract data management for each user. Constructed locally and contents are written back into text file after modification.
    '''

    # Static constants 
    FORMAT = ('{', '\tNAME = ', '\tHP = ', '\tSAT = ', '}') # Per-line format of struct in data
    DELIM = '\n{\n' # Primary delimiter for each struct in file
    SAT_THRESH = (10, 25, 50, 100) # Level thresholds for .comp_sat()
    SAT_LEVELS = ('unsaturated', 'soft sat', 'hard sat', 'soft clip', 'hard clip') # Default names for saturation levels

    # Initialise function
    def __init__(self, name, hp, sat):
      ''' Hard_Points.hp_struct(str, int, str)
      Instantiates an hp_struct object with given username, hard points, and saturation level.
      Inputs are not validated, which will be the responsibility of wrapper class 
      '''
      self.name = name
      self.hp = hp
      self.sat = sat
    
    # Fundamental accessors
    def get_name(self):
      ''' self.get_name() => str
      Returns Discord application username of object
      '''
      return self.name
    
    def get_hp(self):
      ''' self.get_hp() => int
      Returns Hard Points of object
      '''
      return self.hp
    
    def get_sat(self):
      ''' self.get_sat() => str
      Returns Saturation Level of object
      '''
      return self.sat
    
    # Mutators
    async def increment(self, amt=1):
      ''' self.increment(int=amt) => void
      Increments object's HP value once by the given amount, default set to 1, then updates the object's saturation balue
      '''
      self.hp += amt
      await self.comp_sat() # Update saturation level
    
    async def set(self, val=0):
      ''' self.set(*, str=val) => void
      Sets hp value to given value, defaulting to a reset if not given, then updates the object's saturation balue
      '''
      self.hp = val
      await self.comp_sat()

    async def comp_sat(self):
      ''' self.comp_sat() => void
      Compares HP to the class thresholds and changes saturation level accordingly
      '''
      if self.hp >= self.SAT_THRESH[3]:
        self.sat = self.SAT_LEVELS[4]
      elif self.hp >= self.SAT_THRESH[2]:
        self.sat = self.SAT_LEVELS[3]
      elif self.hp >= self.SAT_THRESH[1]:
        self.sat = self.SAT_LEVELS[2]
      elif self.hp >= self.SAT_THRESH[0]:
        self.sat = self.SAT_LEVELS[1]
      else:
        self.sat = self.SAT_LEVELS[0]

    # File accessor
    @staticmethod
    async def read(name):
      ''' Hard_Points.hp_struct.read(str) => [str, int, str]
      Given a Discord username, reads the hp-list file and extracts the attributes of the corresponding struct for that user. Returns None if user not found.
      Static function, not used on self
      '''
      # Open file and gather all contents
      with open('hp_folder/hp-list.txt', 'r') as file:
        # Split contents based on preset delimiter, corresponding to unique users, and remove user list (first element)
        contents = file.read().strip().split(Hard_Points.hp_struct.DELIM)
        # print('for', name, ':\n', contents) # TEST
        contents.pop(0)
        # contents.pop(0)
        # print('read():', contents, len(contents)) # TEST

        # Checks if the given user exists in file system
        for i in range(0, len(contents) + 1):
          # print(ind) # TEST
          if i >= len(contents):
            # Failure case
            # print('failed at', i) # TEST
            raise Exception
          if contents[i].find(name) != -1:
            # print(i, contents[i], name, contents[i].find(name)) #
            break
        # print(i, len(contents)) # TEST
        
        
        await asyncio.sleep(0.1) # Moment of calm

        # Extracts attributes from struct
        breakdown = contents[i].split('\n')
        # print('break', breakdown) # TEST
        name = breakdown[0].lstrip(Hard_Points.hp_struct.FORMAT[1]).strip()
        hp = int(breakdown[1].lstrip(Hard_Points.hp_struct.FORMAT[2]).strip())
        sat = breakdown[2].lstrip(Hard_Points.hp_struct.FORMAT[3]).strip()

        # Returns attributes for use outside of program
        # print(name, hp, sat) # TEST
        return [name, hp, sat]

    # File mutators/save
    async def write(self):
      ''' self.write(self) => void
      Checks if the user exists within filesystem. If so, make edits to the specific file with the updated information from the current object. If not, add the file to the system.
      '''
      # Reads user list (first line) from hp-list
      file = open('hp_folder/hp-list.txt', 'r')
      user_list = file.readline().lstrip('USERS = ').strip().split(', ')
      # print('write()\n', user_list) # TEST

      # Check if user exists in file system
      if self.name in user_list:
        # Edits the file with current object's information
        await self.edit()
      else:
        # Adds the user's information to the file, passing the current user list for convenience
        await self.add(user_list)

    async def add(self, user_list):
      ''' self.add([str]) => void
      Adds the current struct as follows:
      Opens file and separates the file's user list from the rest of current file's contents
      Formats the user list to include the new user
      Creates a formatted string representing the struct for the new user
      Writes the new content into the file
      '''
      # Extracts content files and partition out former user list
      file = open('hp_folder/hp-list.txt', 'r')
      contents = file.read().partition('\n') # (old user-list, rest of contents)
      file.close()
      # print('contents', contents) # TEST

      await asyncio.sleep(0.1) # Moment of calm

      # Write new data into file
      with open('hp_folder/hp-list.txt', 'w') as file:
        # Add user name to user list
        user_list.append(self.name)
        user_line = 'USERS = ' + ', '.join(user_list).lstrip(', ')
        # print(user_line) # TEST

        # Create struct for user
        formatted = list(self.FORMAT)
        formatted[0] = '\n' + formatted[0]
        formatted[1] += self.name
        formatted[2] += str(self.hp)
        formatted[3] += self.sat
        # print('format', '\n'.join(formatted)) # TEST

        # Write new contents into file
        cond = '\n' if contents[2] != '' else ''
        file.write(user_line + cond + contents[2] + '\n'.join(formatted))
    
    async def edit(self):
      ''' self.edit() => void
      Edits hp-list using data from the current struct as follows:
      Opens file, reads contents, splits contents by the delimiter for all structs in file, and separates user_list from contents variable
      Assuming .edit() is called correctly, identifies and stores the index corresponding to the given user's struct in content list
      Fetches and splits that content struct into lines and updates HP and saturation level for corresponding lines
      Replaces index of context list with updates lines and writes lines back into file
      '''
      # Opens file and reads and processes contents
      file = open('hp_folder/hp-list.txt', 'r')
      contents = file.read().strip().split(self.DELIM) # DELIM = '\n{\n'
      file.close()
      user_list = contents[0] # User list remains unchanged
      contents.pop(0) # This is for each of use by following loop to mitigate potential edge cases
      # print(f'edit() for {self.name}:\n', contents) # TEST

      # Identifies the index corresponding to the current object's struct in file
      ind = 0
      for i in range(0, len(contents)):
        if contents[i].find(self.name) != -1:
          ind = i
          # print(i) # TEST
          break # Variable i is saved out of loop
      
      await asyncio.sleep(0.1) # Moment of calm

      # Updates the information within that struct
      breakdown = contents[ind].split('\n') # Line-by-line modification
      # print('break', breakdown) # TEST
      if self.hp != int(breakdown[1].lstrip(self.FORMAT[2]).strip()):
        breakdown[1] = self.FORMAT[2] + str(self.hp)
        breakdown[2] = self.FORMAT[3] + self.sat
      # if self.sat != int(breakdown[2].lstrip(FORMAT[3]).strip()):
      
      # Recombines all lines and writes updated data into file
      contents[ind] = '\n'.join(breakdown)
      # print('post', contents) # TEST
      with open('hp_folder/hp-list.txt', 'w') as file:
        file.write(user_list + self.DELIM + self.DELIM.join(contents))
    
    @staticmethod
    async def delete(name):
      ''' Hard_Points.hp_struct.delete(str) => Bool
      Given a Discord username, removes the user from the hp-list file. Returns True if successful, returns False if user never existed in the first place.
      Static function, not used on self
      '''
      # Open file and gather all contents
      with open('hp_folder/hp-list.txt', 'r') as file:
        # Split contents based on preset delimiter, corresponding to unique users
        contents = file.read().strip().split(Hard_Points.hp_struct.DELIM)
        user_list = contents[0].lstrip('USERS = ').strip().split(', ') # Stores user_list separately to optimize case checking
        contents.pop(0)
        # print('user_list\n', user_list, type(user_list)) # TEST
        
        # Checks if user was registered to file system, and if so, remove name from user_list
        # print(name, user_list.find('')) # TEST
        if name not in user_list:
          return False
        user_list.remove(name)

        await asyncio.sleep(0.1) # Moment of calm

        # Searches file system for given user and removes corresponding struct when found
        for i in range(0, len(contents)):
          if contents[i].find(name) != -1:
            contents.pop(i)
            break
        # print('post', contents)
        
        # Recombines all sections and updates data into file
        with open('hp_folder/hp-list.txt', 'w') as file:
          file.write('USERS = ' + ', '.join(user_list) + Hard_Points.hp_struct.DELIM + Hard_Points.hp_struct.DELIM.join(contents))
        
        # Return value
        return True

  # Private initialisation function
  def init(name, hp=0, sat=None):
    ''' Hard_Points.init(str, int=hp, str=sat) => Hard_Points.hp_struct
    Given the username and the two optional arguments (default arguments 0 for hp and unsaturated for sat), returns a new hp_struct object.
    Meant for internal use
    '''
    # default value for hp is 0, int
    # default value for hp is 'unsaturated', str, referred to by Hard_Points.hp_struct.SAT_LEVELS[0]
    return Hard_Points.hp_struct(name, hp, Hard_Points.hp_struct.SAT_LEVELS[0] if sat == None else sat)

  # Pure initialisation
  async def make(name):
    ''' Hard_Points.new(str) => str
    Assuming user is new to the system, creates a new hp_struct object for the corresponding user, writes it onto file, and returns confirmation output
    '''
    user = Hard_Points.init(name) # Creates new object
    await user.write() # Writes struct into hp-list file
    return f'{name} has been registered into the Hard Points system!'
  
  # General initialisation
  async def new(name):
    ''' Hard_Points.create(str) => str
    Determines if user exists in current file system; if not, adds user to system
    '''
    # Check if user is in current system
    try:
      await Hard_Points.hp_struct.read(name)
    except Exception: # .read() fails to find user and throws and Exception
      # Create new user and add to system
      return await Hard_Points.make(name)
    
    # User already exists
    return f'{name} is already in the Hard Points system.'

  # Accessors
  async def points(name, full=False):
    ''' Hard_Points.points(str, bool=full) => str
    Returns given user's HP (default 0 if user is new) and includes the user's saturation level if full = True 
    '''
    # Check if user is in current system
    try:
      attr = await Hard_Points.hp_struct.read(name)
      # print('Faux', attr) # TEST
    except Exception:
      # Creates new user and writes data into system
      # print(True) # TEST
      user = Hard_Points.init(name)
      await user.write()

      # attr elements ordered and purposed like attr otherwise
      attr = [name, user.get_hp(), user.get_sat()]
    
    # Return confirmation message
    add_on = f' and saturation level \'{attr[2]}\'' if full else ''
    return f'{attr[0]} has {str(attr[1])} HP{add_on}.'
  
  async def sat(name):
    ''' Hard_Points.sats(str) => str
    Returns given user's saturation level (default DELIM[0] if user is new)
    '''
    # Check if user is in current system
    try:
      attr = await Hard_Points.hp_struct.read(name)
      sat = attr[2]
    except:
      # Creates new user and writes data into system
      user = Hard_Points.init(name)
      await user.write() 

      # sat from this context should be same as sat otherwise
      sat = user.get_sat()
    
    # Return confirmation message
    return f'{name} has saturation level \'{sat}\'.'

  async def inc(name):
    ''' Hard_Points.inc(str) => str
    After checking that the user exists within current system, increments their HP by one point and updates value within file
    '''
    # Check if user is in current system
    try:
      # Create new hp_struct from file data
      attr = await Hard_Points.hp_struct.read(name)
      user = Hard_Points.init(attr[0], attr[1], attr[2])
    except Exception:
      # Creates new user object; all other functions are same
      user = Hard_Points.init(name)
    
    # Add + 1 to user's HP
    await user.increment()
    await user.write()

    # Return confirmation
    return f'Gave + 1 HP to {name}!'
  
  async def add(name, amt):
    ''' Hard_Points.inc(str, int) => str
    After checking that the user exists within current system, adds the given amount of points to HP and updates value within file
    '''
    # Check if user is in current system
    try:
      # Create new hp_struct from file data
      attr = await Hard_Points.hp_struct.read(name)
      user = Hard_Points.init(attr[0], attr[1], attr[2])
    except Exception:
      # Creates new object
      user = Hard_Points.init(name)
    
    # Adds amt to user's HP
    await user.increment(amt)
    await user.write()

    # Return confirmation
    return f'Gave {amt} HP to {name}!'
  
  async def set(name, val):
    ''' Hard_Points.set(str, int) => str
    After checking that the user exists within current system, sets HP value to given amount and updates value within file
    '''
    # Check if user is in current system
    try:
      # Create new hp_struct from file data
      attr = await Hard_Points.hp_struct.read(name)
    except Exception:
      # Function does not need to continue further; return failure statement
      return f'{name} does not exist within the HP system.'
    
    # Creates object for user
    user = Hard_Points.init(attr[0], attr[1], attr[2])
    await user.set(val) # Sets HP to value
    await user.write()

    # Return confirmation
    return f'{name}\'s HP has been set to {val}!'
  
  async def reset(name):
    ''' Hard_Points.set(str, int) => str
    After checking that the user exists within current system, resets HP value and updates value within file
    '''
    # Check if user is in current system
    try:
      # Create new hp_struct from file data
      attr = await Hard_Points.hp_struct.read(name)
    except Exception:
      # Return failure statement
      return f'{name} does not exist within the HP system.'
    
    # Creates object for user
    user = Hard_Points.init(attr[0], attr[1], attr[2])
    await user.set(0)
    await user.write()

    # Return confirmation statement
    return f'{name}\'s HP has been reset!'
  
  async def delete(name):
    ''' Hard_Points.delete(str) => str
    Runs .delete() with the given username. If username exists, user information is deleted and a confirmation message is returned. If not, function returns failure statement.
    '''
    return f'{name}\'s data has been expunged.' if await Hard_Points.hp_struct.delete(name) else f'{name}\'s data cannot be delted as {name} never existed.'
