class Ayan:

	def __init__(self):
		self.name = 'Surisun'
		self.lastname = 'chaichai'
		self.nickname = 'Yan'

	def WhoAmI(self):
		print('My name is {}'.format(self.name))
		print('My lastname is {}'.format(self.lastname))
		print('ชื่อไทย: ดวงอาอิตย์ โครตสว่าง')

	@property
	def thainame(self):
		return 'ดวงอาอิตย์ โครตสว่าง'

if __name__ == '__main__':
	mynai = Ayan()
	print(mynai.name)
	print(mynai.lastname)
	mynai.WhoAmI()
	print(mynai.thainame)
