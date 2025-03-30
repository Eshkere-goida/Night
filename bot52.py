import random
nums = ['1','2','3','4','5','6','7','8','9','0']
list1 = []
for n in range(100):
    for i in range(7):
        rand = random.randint(0,9)
        list1.append(nums[rand])
        
    for i in range(7):
        if list1[0]=='0':
            list1[0]='1'
            print(list1[i],end='')
        else:
            print(list1[i],end='')
    list1 = []
    print("\n")