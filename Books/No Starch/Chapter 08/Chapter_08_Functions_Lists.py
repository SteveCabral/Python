from Chapter_08_Modules import VerifyUserList


#create original user list
#list_original = {'alice': False, 'brian': True, 'candace': False}
list_original = ['alice' , 'brian', 'candace']

#confirm users with a copy of the list
list_revised = VerifyUserList(list_original[:]) #call function passing list copy using slice notation [:]

#display the lists
print(f"\nOriginal List:\n{list_original}")
print(f"\nRevised List:\n{list_revised}")


#add david to  original list:
list_original.append('david')

#display the lists
print(f"\nOriginal List:\n{list_original}")
print(f"\nRevised List:\n{list_revised}")