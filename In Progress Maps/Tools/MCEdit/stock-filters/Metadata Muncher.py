# 2021-11-25
# another mcedit filter by connor135246. once again shamelessly stolen from Blockonditional_v2.
# this time, we're going to fix blocks with weird metadata by setting them to the default metadata for the block.
# there are a lot of blocks with weird metadata in the glide maps from legacy console edition, for some reason.
# some blocks (such as stairs) should probably be manually checked afterward to ensure their orientation is correct.
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
		# connor135246
		("Metadata Muncher", "label"), 
		("Fixes weird metadata blocks, usually by setting them to their default metadata. Make sure to check the orientation of blocks like torches and chests afterwards.", "label"),
		("Skip Air blocks", True),
		("Debug (shows each step in console)", False),
		# /connor135246
		
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
		)

def perform(originalLevel, originalBox, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "PERFORM METADATA MUNCHER" # connor135246
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(originalLevel,originalBox,options,method) # Log start
	SUCCESS = False
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))
	boxOrigin = originalBox.origin # connor135246
	# Operations go here - switch to the function based on selected operation
	
	SUCCESS = metadataMuncher(level, box, options, boxOrigin) # connor135246
		
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

# connor135246
def getFixedData((block, data)):
	# torches and (lit) redstone torches don't use metadata 0. 5 is the metadata for a torch sitting on top of a block.
	if block in [50, 75, 76]: 
		return 5
	# wall signs, ladders, (lit) furnaces, chests, trapped chests, and heads don't use metadata 0. 2 is the metadata for facing north.
	elif block in [68, 65, 61, 62, 54, 146, 144]:
		return 2
	# tall grass is a little weird... we'll assume that most of the time, people will use dead bushes when they want dead bushes instead of the unobtainable shrubs.
	elif block == 31:
		return 1
	# big mushroom blocks with metadata 11 are "all outside" in console, but unknown in java. java's "all outside" is metadata 14.
	elif block in [99, 100] and data == 11:
		return 14
	else:
		return 0

def setData(level, x, y, z, data):
	level.setBlockDataAt(x, y, z, data)

def getActualLevelCoordinates(x, y, z, boxOrigin):
	return (x + boxOrigin[0], y + boxOrigin[1], z + boxOrigin[2])
# /connor135246

def metadataMuncher(level,box,options, boxOrigin): # connor135246
	# Local variables
	method = "I MUNCH AND I CRUNCH AND I EAT YOUR WEIRD VALUES" # connor135246
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	SUCCESS = False	

	# connor135246
	SKIPAIR = options["Skip Air blocks"]
	SHOWINFO = options["Debug (shows each step in console)"]
	
	FIXCOUNT = 0
	# /connor135246
	
	for y in xrange(0,height):
		for x in xrange(0,width):
			for z in xrange(0,depth):
				curBlock = getBlock(level, x, y, z)
				
	# connor135246
				if (not SKIPAIR or curBlock[0] != 0) and alphaMaterials[curBlock].name == "Future Block!":
					fixedData = getFixedData(curBlock)
					fixedBlock = (curBlock[0], fixedData)
					if alphaMaterials[fixedBlock].name != "Future Block!":
						setData(level, x, y, z, fixedData)
						FIXCOUNT = FIXCOUNT + 1
						SUCCESS = True
						if SHOWINFO:
							print 'Placed %s at %s, replacing %s' % (alphaMaterials[fixedBlock], getActualLevelCoordinates(x, y, z, boxOrigin), alphaMaterials[curBlock])																
		
	print 'Total Blocks Fixed: %s' % (FIXCOUNT)
	print 'Skipped Air blocks: %s' % (SKIPAIR)
	# /connor135246
	
	FuncEnd(level,box,options,method) # Log end
	return SUCCESS
