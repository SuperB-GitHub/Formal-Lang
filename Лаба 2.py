def Grammar (Pravila:dict):
    N=[]
    T=[]
    for key in Pravila.keys():
        el_dict=Pravila[key]
        for sam_word in el_dict:
            for nom_word in range(len(sam_word)):
                if str(sam_word[nom_word]).isupper() and str(sam_word[nom_word]) not in N:
                    N.append(str(sam_word[nom_word]))
                if str(sam_word[nom_word]) not in N  and str(sam_word[nom_word]) not in T:
                    T.append(str(sam_word[nom_word]))

    for key in Pravila.keys():
        for s_in in key:
            if s_in not in N and str(s_in).isupper():
                N.append(s_in)

    for key_one in Pravila.keys():
        S=key_one
        break
    if 'e' in T:
        T.pop(T.index('e'))
    print(f'G = ({sorted(T)}, {sorted(N)}, P, {S})')
    return [T,N,S]

def Check(Pravila:dict,TN:list):
    types={0:'Нулевой (Свободный)',
           1:'Контекстно-зависимый',
           2:'Контекстно-свободный',
           3:'Регулярный'}
    T=TN[0]
    N=TN[1]
    TN=N+T
    TN.append('e')
    typ=[]

    for key in Pravila.keys():
        for el in Pravila[key]:
            if key in T and ((el[-1] in N and el[0] in T)  or (el[0] in N and el[-1] in T)):
                typ.append(3)
                break
            elif key in N:
                for el_p in el:
                    if el_p in TN:
                        typ.append(2)
            elif len(key)<=len(el):
                typ.append(1)
                break
            else:
                typ.append(0)
    return types[min(typ)]

def Exist(Pravila:dict,TN:list):
    T=TN[0]
    N=TN[1]
    for key in Pravila.keys():
        if key == TN[2]:continue
        check=[]
        for el in Pravila[key]:
            check.append(any(symb in el for symb in T))
        if True in check: 
            continue
        else: return 'Язык не существует'
    return 'Язык существует'

def DontGenSumb(Pravila:dict,TN:list):
    T=TN[0]
    N=TN[1]
    t=[TN[2]]
    n=['e']
    n.extend(T)
    for elem_t in t:
        for elem in Pravila[elem_t]:
            for elem_elem in elem:
                if elem_elem not in t and elem_elem in N:
                    t.append(elem_elem)
    while TN[2] in t:
        for elem_t in t:
            for elem in Pravila[elem_t]:
                check=[]
                for elem_elem in elem:
                    if elem_elem in n:
                        check.append(True)
                    else: check.append(False)
                if False not in check and elem_t not in n:
                    n.append(elem_t)
                    t.pop(t.index(elem_t))             
    for fin_el in t:
        for key in Pravila.keys():
            Prav=[]
            Prav.extend(Pravila[key])
            if fin_el in Prav:
                Prav.pop(Prav.index(fin_el))
            Pravila[key]=Prav
        Pravila.pop(fin_el)


    if t!=[]:
        print(f'\nНепорождающие терминалы: {t}\nНовые правила:')
        return Pravila
    else: return f'\nНепорождающих терминалов нет'

def DontGoSumb(Pravila:dict,TN:list):
    T=TN[0]
    N=TN[1]
    n=[TN[2]]
    u=[]
    for elem_n in n:
        for elem in Pravila[elem_n]:
            for elem_in_elem in elem:
                if elem_in_elem not in n and elem_in_elem in N:
                    n.append(elem_in_elem)
                elif elem_in_elem not in u and elem_in_elem in T:
                    u.append(elem_in_elem)
    f_n=[] #Мн-во не достижимых терминалов
    for elem in N:
        if elem not in n:
            f_n.append(elem)
    f_u=[] #Мн-во не достижимых не терминалов
    for elem in T:
        if elem not in u:
            f_u.append(elem)
    for elem in f_n:
        Pravila.pop(elem)

    if f_n!=[]:
        print(f'\nНедостижимые символы: {f_n} и {f_u}\nНовые правила:')
        return Pravila
    else: return f'\nНедостижимых символов нет'

def DelERule(Pravila:dict,TN:list):
    T=TN[0]
    N=TN[1]
    E=list
    u=1
    while u==1:
        for key in Pravila.keys():
            for elem in Pravila[key]:
                if elem == 'e' or elem in E:
                    E.append(key)
    return

P={}
u=True
print('Введите правила:')
while u==True:
    try:
        key, prav=input().split()
        P[key]=prav.split(',')
    except:
        u=False
print('Правила: \nP =',P)
print('Грамматика: ')
TN=Grammar(P)
print('Проверка типа: ',Check(P,TN))
print('Проверка на существование: ', Exist(P,TN))
print(DontGenSumb(P,TN))
TN=Grammar(P)
print(DontGoSumb(P,TN))
TN=Grammar(P)