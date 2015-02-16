import sgmllib
from datetime import date

def sum_values(trnlist):
	return sum([trn.amount for trn in trnlist])

def strip_transfers(trnlist):
	return filter(lambda x: not(x.sibling), trnlist)

def amalgamate(account_list):
	a = Account()
	for j in account_list:
		a.combine(j)
	return a

def sep_month(trnlist):
	h = {}
	for trn in trnlist:
		month = trn.date.month
		if not h.has_key(month):
			h[month] = []
		h[month].append(trn)
	return h

def label_transfers(accountlist):
	for account in accountlist[0:-1]:
		for otheracct in accountlist[accountlist.index(account)+1:]:
			for trn1 in account.trns:
				for trn2 in otheracct.trns:
					if (abs((trn1.date - trn2.date).days) < 2 and trn1.amount == -trn2.amount):
						# these probably go together.
						trn1.sibling = trn2
						trn2.sibling = trn1

def overall_by_month(account):
	by_month(account, lambda x: True)

def spending_by_month(account):
	by_month(account, lambda x: x.amount < 0)

def earnings_by_month(account):
	by_month(account, lambda x: x.amount > 0)

def by_month(account, f):
	t = strip_transfers(account.trns)
	h = sep_month(t)
	print h
	for month in h:
		print month, sum_values([ x for x in h[month] if f(x)])


def print_trns(trns):
	for i in range(len(trns)):
		print "%3d: %s" % (i, trns[i].to_string())
	
class Transaction:
	def __init__(self):
		self.type = "POS"
		self.amount = 0
		self.name = "Transaction"
		self.memo = ""
		self.id = 0
		self.date = '20000000'
		self.sibling = None
		self.account = None
		self.tags = []
	def to_string(self):
		if (self.amount > 0):
			amt = "+$%s" % self.amount
		else:
			amt = "-$%s" % abs(self.amount)
		return "%8s, %-10s,  %-25s, %s" % (self.date, amt, self.name, self.memo)

class Account:
	def __init__(self):
		self.trns = []
		self.bankid = 0
		self.id = 0
		self.start_date = 0
		self.end_date = 0
		self.balance = 0
		self.type = 0
	def combine(self, acct):
		self.balance += acct.balance
		self.trns.extend(acct.trns)
		self.trns.sort(key = lambda x: x.date)
	def list(self):
		for i in range(len(self.trns)):
			print "%3d: %s" % (i, self.trns[i].to_string())
	def description(self):
		return  "%s account, id %s, with balance %s" % (self.type, self.id, self.balance)

class ofxparser(sgmllib.SGMLParser):
	def start_ofx(self, data):
		self.accounts = []
	
	def start_stmttrn(self, data):
		self.curtrn = Transaction()
		self.curtrn.account = self.curacct

	def end_stmttrn(self):
		self.curacct.trns.append(self.curtrn)

	def start_bankacctfrom(self, data):
		self.curacct = Account()

	def start_ledgerbal(self, data):
		pass
	def start_ccacctfrom(self, data):
		self.curract = Account()
		self.curacct.type = "Credit Card"
	def end_ledgerbal(self):
		self.accounts.append(self.curacct)
		self.curacct = Account()
	def parse(self, filename):
		self.feed(open(filename).read())
		self.close()
		return self.accounts
	
	def handle_data(self, data):
		data = data.strip()
		if not (data and self.get_starttag_text()):
			return
		tag = self.get_starttag_text()[1:-1].lower()
		if (tag == "trntype"):
			self.curtrn.type = data
		elif (tag == "trnamt"):
			self.curtrn.amount = float(data)
		elif (tag == "name"):
			self.curtrn.name = data
		elif (tag == "memo"):
			self.curtrn.memo = data
		elif (tag == "fitid"):
			self.curtrn.id = data
		elif (tag == "dtposted"):
			self.curtrn.date = date(int(data[0:4]), int(data[4:6]), int(data[6:8]))
		elif (tag == "bankid"):
			self.curacct.bankid = data
		elif (tag == "acctid"):
			self.curacct.id = data
		elif (tag == "dtstart"):
			self.curacct.start_date = data
		elif (tag == "dtend"):
			self.curacct.end_date = data
		elif (tag == "balamt"):
			self.curacct.balance = float(data)
		elif (tag == 'accttype'):
			self.curacct.type = data.capitalize()
		else: 
			pass
parser = ofxparser()
acctlist = parser.parse('ofx50081.qfx')
label_transfers(acctlist)
#acctlist = parser.parse('ofx24986.ofx')
