file = open('numbers.txt','rt',encoding='utf-8')
cont = file.readlines()
nums1 = []
nums2 = []

for i in range(1):
    for j in range(len(cont[0])):
        if cont[i][j].isdigit()==True:
            nums1.append(cont[i][j])
for i in range(1):
    for j in range(len(cont[1])):
        if cont[i][j].isdigit()==True:
            nums2.append(cont[i][j])

for i in range(len(nums1)):
    num1 = ''
    num1+=nums1[i]
for i in range(len(nums2)):
    num2 = ''
    num2+=nums2[i]

 

print(int(num1)+int(num2))
