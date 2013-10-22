import decimal, urllib
from django.conf import settings
import .models

class Verify( object ):
	'''builds result, results, response'''
	def __init__( self, tx ):
		try:
			transaction = models.Purchase.objects.get( tx=tx )
			self.result = 'Transaction %s has already been processed' % tx
			self.response = self.result
		except models.Purchase.DoesNotExist:
			post = dict()
			post[ 'cmd' ] = '_notify-synch'
			post[ 'tx' ] = tx
			post[ 'at' ] = settings.PAYPAL_PDT_TOKEN
			self.response = urllib.urlopen( \
				settings.PAYPAL_PDT_URL, urllib.urlencode(post)).read()
			print 'response: ' + str(self.response)
			lines = self.response.split( '\n' )
			self.result = lines[0].strip()
			self.results = dict()
			for line in lines[1:]: # skip first line
				linesplit = line.split( '=', 2 )
				if len( linesplit ) == 2:
					self.results[ linesplit[0].strip() ] = \
						urllib.unquote(linesplit[1].strip())

	def success( self ):
		return self.result == 'SUCCESS' and \
			self.results[ 'payment_status' ] == 'Completed'

	def amount( self ):
		return decimal.Decimal(self.results[ 'payment_gross' ])
			

