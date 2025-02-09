

list1 = input().split()
list2 = []
for i in list1:
    if i not in list2:
         list2.append(i)
print(list2)

list2 = []
dict1 = {'a': 'abc', 'b': 'defgh', 'i': 'j', 'kl': 'mnopqr'}

max_length = 0
max_key = ''
for key, value in dict1.items():
        current_length = len(value)  
        if current_length > max_length:  
            max_length = current_length
            max_key = key
print(max_key)