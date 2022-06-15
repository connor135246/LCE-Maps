# 2021-11-23
# some simple edits by connor135246 for my own purposes. 
# like the original, it finds a block and places another block near it.
# the first difference is that it has options for ignoring the metadata of the find block and the replace only block.
# the second difference is instead of an offset, you choose what combination of the six surrounding blocks will be affected.
# i've marked added/changed lines with # connor135246
# original description:
#
# This filter is for conditionally replacing blocks in a selection area per @cocoamix86.
# 21/9/2015 - init
# abrightmoore@yahoo.com.au
# Modified to add "replace only" functionality by ZungryWare.
# http://brightmoore.net
# My filters may include code and inspiration from PYMCLEVEL/MCEDIT mentors @Texelelf, @Sethbling, @CodeWarrior0, @Podshot_

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, cosh
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long, TileEntity
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
from copy import deepcopy
import bresenham # @Codewarrior0
from random import Random # @Codewarrior0

inputs = (
		("BLOCKONDITIONAL (Six sides edit)", "label"), # connor135246
		("Find block:", alphaMaterials.Grass),
		("Place block:", alphaMaterials.Stone),
		("Replace only:", alphaMaterials.Air),
		("Use Replace only?", True),
		
		# connor135246
		("Ignore Metadata of Find block?", False), 
		("Ignore Metadata of Replace only block?", False), 
		("Up (+Y)", True), 
		("Down (-Y)", True), 
		("North (-Z)", True), 
		("South (+Z)", True),
		("East (+X)", True), 
		("West (-X)", True),
		("Debug (shows each step in console)", False),
		# /connor135246
		
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
		)

def perform(originalLevel, originalBox, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "PERFORM BLOCKONDITIONAL"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(originalLevel,originalBox,options,method) # Log start
	SUCCESS = False
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))
	boxOrigin = originalBox.origin # connor135246
	# Operations go here - switch to the function based on selected operation
	
	SUCCESS = blockonditional(level, box, options, boxOrigin) # connor135246
		
	# Conditionally copy back the working area into the world
	if SUCCESS == True: # Copy from work area back into the world
		b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)

	FuncEnd(originalLevel,originalBox,options,method) # Log end
	
def FuncStart(level, box, options, method):
	# abrightmoore -> shim to prepare a function.
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	centreWidth = math.floor(width / 2)
	centreHeight = math.floor(height / 2)
	centreDepth = math.floor(depth / 2)	
	# other initialisation methods go here
	return (method, (width, height, depth), (centreWidth, centreHeight, centreDepth))

def FuncEnd(level, box, options, method):
	print '%s: Ended at %s' % (method, time.ctime())

def getBlock(level,x,y,z):
	return (level.blockAt(x,y,z), level.blockDataAt(x,y,z))

def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)

# connor135246
# i know minecraft already has some way of ordering the six directions from 0 to 5 but i can't be bothered to look it up so the order here is:
# 0 = Up (+Y)
# 1 = Down (-Y)
# 2 = North (-Z)
# 3 = South (+Z)
# 4 = East (+X)
# 5 = West (-X)
def offsetCoordsByDirection(x, y, z, direction):
	return [x + (1 if direction == 4 else (-1 if direction == 5 else 0)), y + (1 if direction == 0 else (-1 if direction == 1 else 0)), z + (1 if direction == 3 else (-1 if direction == 2 else 0))]

def getActualLevelCoordinates(x, y, z, boxOrigin):
	return (x + boxOrigin[0], y + boxOrigin[1], z + boxOrigin[2])
# /connor135246

def blockonditional(level,box,options, boxOrigin): # connor135246
	# Local variables
	method = "BLOCKONDITIONAL"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	SUCCESS = False	

	FINDBLOCK = getBlockFromOptions(options,"Find block:")
	PLACEBLOCK = getBlockFromOptions(options,"Place block:")
	REPLACEBLOCK = getBlockFromOptions(options,"Replace only:")
	USEREPLACE = options["Use Replace only?"]
	
	# connor135246
	IGNOREMETAFIND = options["Ignore Metadata of Find block?"]
	IGNOREMETAREPLACE = options["Ignore Metadata of Replace only block?"] 
	UP = options["Up (+Y)"] 
	DOWN = options["Down (-Y)"] 
	NORTH = options["North (-Z)"] 
	SOUTH = options["South (+Z)"] 
	EAST = options["East (+X)"] 
	WEST = options["West (-X)"] 
	DIRECTIONS = [UP, DOWN, NORTH, SOUTH, EAST, WEST]
	SHOWINFO = options["Debug (shows each step in console)"]

	if not (UP or DOWN or NORTH or SOUTH or EAST or WEST):
		print 'ERROR: At least one Direction box must be checked...'
		FuncEnd(level,box,options,method)
		return False
	
	MATCHCOUNT = 0
	PLACECOUNT = 0
	# /connor135246
	
	for y in xrange(0,height):
		for x in xrange(0,width):
			for z in xrange(0,depth):
				curBlock = getBlock(level, x, y, z)
				
	# connor135246
				if curBlock[0] == FINDBLOCK[0] and (IGNOREMETAFIND or curBlock[1] == FINDBLOCK[1]):
					MATCHCOUNT = MATCHCOUNT + 1
					curPC = PLACECOUNT
					if SHOWINFO:
						print 'Matched %s at %s' % (alphaMaterials[curBlock], getActualLevelCoordinates(x, y, z, boxOrigin))
					for direction in range(len(DIRECTIONS)):
						if DIRECTIONS[direction]:
							offsetCoords = offsetCoordsByDirection(x, y, z, direction)
							checkBlock = getBlock(level, offsetCoords[0], offsetCoords[1], offsetCoords[2])
							if not USEREPLACE or (checkBlock[0] == REPLACEBLOCK[0] and (IGNOREMETAREPLACE or checkBlock[1] == REPLACEBLOCK[1])):
								setBlock(level, PLACEBLOCK, offsetCoords[0], offsetCoords[1], offsetCoords[2])
								SUCCESS = True
								PLACECOUNT = PLACECOUNT + 1
								if SHOWINFO:
									print 'Placed %s at %s, replacing %s' % (alphaMaterials[PLACEBLOCK], getActualLevelCoordinates(offsetCoords[0], offsetCoords[1], offsetCoords[2], boxOrigin), alphaMaterials[checkBlock])								
					if SHOWINFO and curPC == PLACECOUNT:
						print 'Didn\'t place any blocks this time'
	
	print 'Total Blocks Found: %s' % (MATCHCOUNT)
	print 'Total Blocks Placed: %s' % (PLACECOUNT)
	# /connor135246
	
	FuncEnd(level,box,options,method) # Log end
	return SUCCESS
