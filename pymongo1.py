from pymongo import MongoClient

client=MongoClient('localhost', 27017)
db=client.empdata

def main():
	while(1):
		selection=raw_input('\n1.Insert\n2.Update\n3.Read\n4.Delete\n0.Exit')

		if(selection=='1'):
			insert()
		elif(selection=='2'):
			update()
		elif(selection=='3'):
			read()
		elif(selection=='4'):
			delete()
		elif(selection=='0'):
			break

		else:
			print('\nWrong choice entered!!! Exit now')
			exit()

def insert():
	try:
		empid=raw_input('Enter employee ID: ')
		empname=raw_input('Enter name: ')
		empage=raw_input('Enter Age: ')
		empco=raw_input('Enter employee country: ')
		empem=raw_input('Enter email-id: ')

		db.Employees.insert_one(
			{
				"id":empid,
				"name":empname,
				"age":empage,
				"country":empco,
				"email":empem
			})
		print '\nInserted data successfully\n'
	except Exception, e:
		print str(e)

def update():
	try:
		criteria=raw_input('Enter ID to be updated\n')
		empname=raw_input('Enter name\n')
		empage=raw_input('Enter Age\n')
		empco=raw_input('Enter employee country\n')
		empem=raw_input('Enter email-id')

		db.Employees.update_one({
				"id":critera},
				{
				"$set":{
					"name":empname,
					"age":empage,
					"country":empco,
					"email":empem
					}
			})
		print '\nRecords updated successfully\n'

	except Exception, e:
		print str(e)

def read():
	try:
		empcol=db.Employees.find()
		print '\nAll data from database\n\n'		
		for emp in empcol:
			#print emp["name"]
			#print emp["email"]
			print emp

	except Exception, e:
		print str(e)

def delete():
	try:
		criteria=raw_input('Enter ID to be deleted: ')
		db.Employees.delete_many({"id":criteria})
		print '\nDeletion Successful!!\n'

	except Exception, e:
		print str(e)

main()

