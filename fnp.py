# File Name Patcher / ESFilenamePatcher Prototype

import os

def fnFilter(fn):
	charArr = {':', ';', '[', ']', '{', '}', '|', '\\', '?', '/', '<', '>', '!'}
	for char in charArr: 
		fn = fn.replace(char, "")
	return fn

class fnpHandler:
	pipeline	= []
	path		= './'
	countImg	= 0
	countVid	= 0

	# class constructor
	def __init__(self):
		print ("##### ESFilename Patcher #####")
		print ("##### Version 0.2 #####")
		print ("Initializing ....")
		self.setDirectory()

	# set workgin directory for win
	def setDirectory(self, dir = ""):
		if not dir:
			self.path = os.getcwd()
		else:
			self.path = dir
		print ("")
		print ("Set directory: " + self.path)

	def setPipeline(self, pl):
		self.pipeline.append(pl)

	def init(self):
		print("Loading pipeline...")
		for x in self.pipeline:
			x.setup()
	
	def dispatch(self):
		# self.path = "C:\\python\\app\\fnp2\\test" #######
		print ('')
		print ('----------------------------------------')
		print ('Summary')
		# generate summary
		for y in self.pipeline:
			y.summary()
		print ('Folder: ' + self.path + '\\')
		print ('----------------------------------------')
		print ('')
		confirm = input('Confirm [Y/n]? ');
		print ('')
		if confirm == 'Y' or confirm == 'y' or confirm == '':
			print ('Processing ...')
			# Patching file name
			pathArr = self.path.split("\\")
			pathLen = len(pathArr)
			list = os.listdir(self.path)
			fnHandler = ESFnHandler(list)

			for fname in list:
				# tmp name
				tmpName = ''
				fnameb = fname.split(".")
				if len(fnameb) > 1:
					fnamec = fname.replace('.'+fnameb[len(fnameb)-1], '')
					for y in self.pipeline:
						tmpName = tmpName + y.patch(fnamec) + ' '
				tmpName = fnHandler.appendUniqueName(fname, tmpName)
				if fnHandler.fnameValidate(fname):
					if fname == tmpName:
						print('[' + fname + '] Do nothing')
					else:
						print('[' + fname + '] Rename to \'' + tmpName + '\'')
						os.rename(self.path + '\\' + fname, self.path + '\\' + tmpName);
				else:
					print('[' + fname + '] Skipped')
			print('')
			print('Done')
			# End		
		else:
			print('Terminated')

# pipeline, abstract class
class fnpPipeline:
	def setup(self):
		pass
	def patch(self, fn):
		return ''
	def summary(self):
		pass

# time
class pipelineTime(fnpPipeline):
	def setup(self):
		import datetime
		newTime = datetime.datetime.now()
		defTime = newTime.strftime("%Y%m%d")
		self.ptTime = input("Please choose a date [" + defTime + "] : " )
		if len(self.ptTime) == 0:
			self.ptTime = defTime
		self.ptTime = fnFilter(self.ptTime)
	def summary(self):
		print ('Date: ' + self.ptTime)
	def patch(self, fn):
		return self.ptTime

# title
class pipelineTitle(fnpPipeline):
	def setup(self):
		path = os.getcwd()
		pathArr = path.split("\\")
		pathLen = len(pathArr)
		if pathLen >= 3:
			titleDef = pathArr[pathLen-3]
		else:
			titleDef = ""
		self.title = input("Please choose a protocol [" + titleDef + "] : " )
		if len(self.title) == 0:
			self.title = titleDef
		self.title = fnFilter(self.title)
	def patch(self, fn):
		return self.title
	def summary(self):
		print ('Protocol: ' + self.title)

# condition
class pipelineCondition(fnpPipeline):
	def setup(self):
		path = os.getcwd()
		pathArr = path.split("\\")
		pathLen = len(pathArr)
		if pathLen >= 3:
			conditionDef = pathArr[pathLen-1]
			if conditionDef.lower() != 'frozen' and conditionDef.lower() != 'ambient' and conditionDef.lower() != 'refrigerated':
				conditionDef = 'ambient'
		else:
			conditionDef = ""
		self.condition = input("Please choose a shipping condition [" + conditionDef + "] : " )
		if len(self.condition) == 0:
			self.condition = conditionDef
		self.condition = fnFilter(self.condition)
	def patch(self, fn):
		return self.condition
	def summary(self):
		print ('Condition: ' + self.condition)

# manage file name
class ESFnHandler:
	countImg = 0
	countVid = 0
	fnRules = {}
	def __init__(self, list):
		self.list = list
	def appendUniqueName(self, name, prefix):
		fnameb = name.split(".")
		if len(fnameb) > 1:
			extension = fnameb[len(fnameb)-1]
			if extension == "JPG" or extension == "jpg" :
				return prefix + self.getImageID() + '.' + extension
			elif extension == "MP4" or extension == "mp4" or extension == "MOV" :
				return prefix + self.getVideoID() + '.' + extension
		return name
	# get a unique id for image file
	def getImageID(self, prefix = 'pic'):
		self.countImg = self.countImg + 1
		return prefix + str(self.countImg)
	# get a video id for image file
	def getVideoID(self, prefix = 'video'):
		self.countVid = self.countVid + 1
		return prefix + str(self.countVid)
	# file name filter
	def fnameValidate(self, fname):
		if len(self.fnRules) == 0:
			# no rules
			return True
		else:
			# match rules
			import re
			for p in self.fnRules:
				cr = re.compile(p)
				if cr.match(fname):
					return True
			return False

# Init program
fnpObj = fnpHandler()

# display pipeline options
print ("")
print ("Available settings:")
print ("[1] Default")
print ("")

defPipeline = "1"
pipeline = input("Please choose a setting [" + str(defPipeline) + "] : " )
if pipeline == '' or pipeline == 1:
	# pipeline 1
	print ("")
	print ("OK")
	print ("")
	fnpObj.setPipeline(pipelineTime())
	fnpObj.setPipeline(pipelineTitle())
	fnpObj.setPipeline(pipelineCondition())
	fnpObj.init()
	fnpObj.dispatch()
else:
	print ("")
	print ('Empty pipeline')
	print ('Terminating...')

import time
time.sleep(5)