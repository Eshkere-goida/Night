import math
list1 = ['2022-22-22 Reeer','7443-43-34 Error','2210-46-34 jitrh']   #3

def find_logs(list):
    dict1 = {}
    
    for i in range(len(list)):
        mx = 0
        for j in range(len(list[i])):
            if list[i][j] in ['1','2','3','4','5','6','7','8','9','0'] or list[i][j] == '-':
                if j>mx:
                    mx=j
                    print(mx)

        dict1[list[i][:mx+1]]=list[i][mx+2:]
    print(dict1)

find_logs(list1)
    
        



list1 = [{'Product':'Teapot'},{'Price':50},{'Quantity':40},{'Product':'Plate'},{'Price':20},{'Quantity':10}]

def find_value(list):     #4
    list_for_products = []
    sum = 1
    temp = 0
    for i in range(len(list)):
        for j in list[i]:
            is_int = isinstance(list[i][j],int)
            if  is_int== True:
                sum*=list[i][j]
                temp+=1
                if temp ==2:
                    print(list_for_products[math.floor(i/3)],'-',sum)
                    
                    sum = 1
                    temp = 0
            else:
                list_for_products.append(list[i][j])

find_value(list1)




list1 = input().split()   #5
list2 = input().split()

def find_pairs(list,list1):
    list_for_pairs = []
    for i in range(len(list)):
        for j in range(len(list1)):
            list_for_pairs.append(tuple(list[i]+'-'+list1[j]))
    print(*set(list_for_pairs))


find_pairs(list1,list2)




list1 = ['qwe','abc','uig']  #9
def find_anagrams(list1):
    dict1 = {}
    for i in range(len(list1)):
        anagram = str(set(list(list1[i])))
        dict1[anagram] = list1[i]
    print(dict1)

find_anagrams(list1)



str1 = input()     #10
list1 = str1.split()

def find_most_used(str1,list2):
    list1 = []
    mx = 0
    for i in range(len(list2)):
        count = str1.count(list2[i])
        name = list2[i]
        list1.append(name+'-'+str(count))
    set1 = set(list1)
    listlist = list(set1)
    for i in range(len(listlist)):
        if int(listlist[i][-1])>mx:
            mx = int(listlist[i][-1])
            th = listlist[i]
            del listlist[i]
            listlist.insert(0,th)


    print(listlist)


find_most_used(str1,list1)




text = input()     #11

def analyze_text_case_sensitive(text):
    words = text.split()
    word_positions = {}
    for position, word in enumerate(words):
        lower_word = word.lower()
        if lower_word not in word_positions:
            word_positions[lower_word] = []
        word_positions[lower_word].append(position)
    return word_positions



result = analyze_text_case_sensitive(text)
print(result)


full_name = input()      #12

def create_secret_name(full_name):
    
    replacement_dict = {
        'а': '@',
        'б': '6',
        'в': '8',
        'е': '3',
        'з': '3',
        'и': '|',
        'к': '|<',
        'л': '|_',
        'о': '0',
        'с': '$',
        'т': '7',
        'я': '9'
    }
    list1 = []
    for i in range(len(full_name)):
        if full_name[i].lower() in replacement_dict:
            list1.append(replacement_dict[full_name[i].lower()])
        else:
            list1.append(full_name[i])
    
    secret_name = ''
    for i in range(len(list1)):
        secret_name+=list1[i]
    print(secret_name)
        




create_secret_name(full_name)



expression = input()


def calculate_expression(expression):    #13
    try:
        
        parts = expression.split()
        
        
        if len(parts) != 3:
            raise ValueError("Некорректный формат выражения. Используйте формат 'число оператор число'")
        
        num1_str, operator, num2_str = parts
        
        
        try:
            num1 = float(num1_str)
            num2 = float(num2_str)
        except ValueError:
            raise ValueError("Операнды должны быть числами")
        
        
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                raise ZeroDivisionError("Деление на ноль невозможно")
            result = num1 / num2
        else:
            raise ValueError(f"Неподдерживаемый оператор: '{operator}'. Поддерживаются: +, -, *, /")
        
        
        return int(result) if result.is_integer() else result
    
    except Exception as e:
        return f"Ошибка: {str(e)}"


print(calculate_expression(expression))



import random

def run_quiz():        #14

    questions = {
        "Какая столица Франции?": "Париж",
        "Сколько планет в Солнечной системе?": "8",
        "Какой язык программирования мы используем?": "Python",
        "Кто написал 'Войну и мир'?": "Толстой",
        "Как называется самая большая планета Солнечной системы?": "Юпитер",
        "В каком году началась Вторая мировая война?": "1941",
        "Какой химический элемент обозначается как 'O2'?": "Кислород",
        "Сколько континентов на Земле?": "6",
        "Какая самая длинная река в мире?": "Амазонка",
    }
    
    
    selected_questions = random.sample(list(questions.items()), 5)
    
    correct_answers = 0
    
    print("Добро пожаловать в викторину! Ответьте на 5 вопросов:\n")
    
    for question, correct_answer in selected_questions:
        print(question)
        user_answer = input("Ваш ответ: ").strip()
        
       
        if user_answer.lower() == correct_answer.lower():
            print("Правильно!\n")
            correct_answers += 1
        else:
            print(f"Неправильно. Правильный ответ: {correct_answer}\n")
    
   
    print(f"Викторина завершена! Ваш результат: {correct_answers} из 5")
    
  
    if correct_answers == 5:
        print("Отлично! Вы знаток!")
    elif correct_answers >= 3:
        print("Хороший результат!")
    else:
        print("Попробуйте еще раз!")


run_quiz()



import random    #15

length = int(input())
complexity = input()
list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
list2 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
list3 = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']

def generate_password(length,complexity):
    password = []
    password1 = ''
    if complexity=='Easy':
        for i in range(length):
            z = random.randint(0,len(list1)-1)
            password.append(list1[z])
            del list1[z]
    elif complexity == 'Medium':
        for i in range(length-1):
            z = random.randint(0,len(list1)-1)
            x = random.randint(0,len(list2)-1)
            y = random.randint(0,len(list3)-1)
            password.append(list1[z])
            del list1[z]
            password.append(list2[x])
    elif complexity == 'Hard':
        for i in range(length-2):
            z = random.randint(0,len(list1)-1)
            x = random.randint(0,len(list2)-1)
            y = random.randint(0,len(list3)-1)
            password.append(list1[z])
            del list1[z]
            password.append(list2[x])
            password.append(list3[y])
    

    for i in range(length):
        password1+=password[i]

    print(password1)

generate_password(length,complexity) 







import random    #17

def assign_roles(students):
    
    if len(students) < 3:
        print("Ошибка: нужно минимум 3 ученика")
        return
    
   
    chosen = random.sample(students, 3)
    
   
    roles = {
        "Ведущий": chosen[0],
        "Помощник": chosen[1],
        "Зритель": chosen[2]
    }
    
    for role, student in roles.items():
        print(f"{role}: {student}")


students = ["Алексей", "Мария", "Иван", "Екатерина", "Дмитрий", "Ольга", "Сергей"]


assign_roles(students)




file1 = open('numbers.txt','r',encoding='utf-8')    #19



def find_python_lines(file):
    lines = file.readlines()
    python_lines = []
    for i in range(len(lines)):
        if 'python' in lines[i].lower():
            python_lines.append((i,lines[i].strip()))
    if len(python_lines)==0:
        print("Слова Python во всех строках не обнаружено")
    else:
        for i in range(len(python_lines)):
            print(*python_lines[i])
    

find_python_lines(file1)