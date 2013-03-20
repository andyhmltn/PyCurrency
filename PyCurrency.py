import urllib2, json, time, glob, os

class PyCurrency:

	# Constructor
	def __init__(self, cachable = True, cacheFolder = 'cache', cacheTimeout = 3600):
		if not os.access(cacheFolder, os.F_OK):
			cachable = False

		if cachable:
			self.cachable     = True
			self.cacheFolder  = cacheFolder
			self.cacheTimeout = 3600

	# Performs conversion
	def convert(self, amount, fromCurrency, toCurrency, rounded = False):
		
		if self.validateCurrency([fromCurrency, toCurrency]) is False:
			raise NameError('Invalid currency code!')

		# Get rate
		rate = self.getRate(fromCurrency, toCurrency)

		converted = rate * amount

		if rounded:
			return round(float(converted), 2)
		else:
			return converted

	# Calculates amount needed in currency to achieve finish currency
	def amountTo(self, finalAmount, fromCurrency, toCurrency, rounded = False):
		finalAmount = float(finalAmount)

		if finalAmount == 0:
			return 0

		if self.validateCurrency([fromCurrency, toCurrency]) is False:
			raise NameError('Invalid currency code!')

		rate = self.getRate(fromCurrency, toCurrency)

		amount = finalAmount / float(rate)

		if rounded:
			return round(amount, 2)
		else:
			return amount


	# Returns the rate
	def getRate(self, fromCurrency, toCurrency):
		rate = self.getCache(fromCurrency + toCurrency)

		if not rate:
			fetch = self.fetch(1, fromCurrency, toCurrency)
			rate = fetch['rate']

			# Cache this rate
			self.newCache(fromCurrency.upper() + toCurrency.upper(), rate)

		return rate

	# Fetches data from API
	def fetch(self, amount, fromCurrency, toCurrency):
		URL = 'http://rate-exchange.appspot.com/currency?q=' + str(amount) + \
			'&from=' + fromCurrency + '&to=' + toCurrency
		response = urllib2.urlopen(URL)
		data = json.load(response) 
		
		return data

	# Checks if rate is cached and returns rate
	# Will return False if cache does not exist our data is timedout
	# 
	# fileName should be currencies concat'd 
	def getCache(self, fileName):

		if self.cachable is not True:
			return False

		path = self.cacheFolder + '/' + fileName + '.convertcache'

		# Check if file exists
		try:
			with open(path): pass
		except IOError:
			return False

		# Array of lines
		f = open(path).readlines() 

		# Check if cache is too old
		if float(f[0]) < (time.time() - self.cacheTimeout):
			return False

		# Return the rate
		return f[1]

	# Validates the currency codes
	# Argument should be an array of the code(s) 
	def validateCurrency(self, codes):
		for code in codes:
			if len(code) != 3 or code.isalnum() is False:
				if code.upper() != 'BEAC':
					return False


		return True

	# Makes a new cache file
	# fileName should be currency codes in caps, FROMTO (i.e. GBPUSD)
	def newCache(self, fileName, rate):
		if self.cachable:
			data = str(time.time()) + '\n' + str(rate)
			f = open(self.cacheFolder + '/' + fileName.upper() + '.convertcache', 'w')
			f.write(data)
			f.close()

	# Deletes all cached files
	def clearCache(self):
		os.chdir(self.cacheFolder)
		fileList  = glob.glob('*.convertcache')
		for cache in fileList:
			os.remove(cache)