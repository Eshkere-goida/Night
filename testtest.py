
n = int(input())
set_list = []

for i in range(n):
    n1 = input()
    l = list(n1)
    set_list.append(set(l))

for i in range(len(set_list)-1):
    intersect = set(set_list[i]).intersection(set(set_list[i+1]))

print(intersect)
