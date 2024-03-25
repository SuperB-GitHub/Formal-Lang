def Grammar (Pravila:dict):
    T=[]
    N=[]
    for key in Pravila.keys():
        el_dict=Pravila[key]
        for sam_word in el_dict:
            for nom_word in range(len(sam_word)):
                if str(sam_word[nom_word]).isupper() and str(sam_word[nom_word]) not in T:
                    T.append(str(sam_word[nom_word]))
                if str(sam_word[nom_word]) not in T  and str(sam_word[nom_word]) not in N:
                    N.append(str(sam_word[nom_word]))

    for key in Pravila.keys():
        for s_in in key:
            if s_in not in T and str(s_in).isupper():
                T.append(s_in)

    for key_one in Pravila.keys():
        S=key_one
        break
    if 'e' in N:
        N.pop(N.index('e'))
    print(f'G = ( {sorted(T)}, {sorted(N)}, P, {S})')
    return [T,N,S]

def Check(Pravila:dict,TN:list):
    types={0:'Нулевой (Свободный)',
           1:'Контекстно-зависимый',
           2:'Контекстно-свободный',
           3:'Регулярный'}
    T=TN[0]
    N=TN[1]
    TN=T+N
    TN.append('e')
    typ=[]

    for key in Pravila.keys():
        for el in Pravila[key]:
            if key in N and ((el[-1] in T and el[0] in N)  or (el[0] in T and el[-1] in N)):
                typ.append(3)
                break
            elif key in T:
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
            check.append(any(symb in el for symb in N))
        if True in check: 
            continue
        else: return 'Язык не существует'
    return 'Язык существует'

def DontGenSumb(Pravila:dict,TN:list):
    T=TN[0]
    N=TN[1]
    t=[TN[2]]
    n=['e']
    n.extend(N)
    for elem_t in t:
        for elem in Pravila[elem_t]:
            for elem_elem in elem:
                if elem_elem not in t and elem_elem in T:
                    t.append(elem_elem)
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
    return t





def DontGoSumb(Pravila:dict,TN:list):
    T=TN[0]
    N=TN[1]
    n=[TN[2]]
    u=[]
    for elem_n in n:
        for elem in Pravila[elem_n]:
            for elem_in_elem in elem:
                if elem_in_elem not in n and elem_in_elem in T:
                    n.append(elem_in_elem)
                elif elem_in_elem not in u and elem_in_elem in N:
                    u.append(elem_in_elem)
    f_n=[] #Мн-во не достижимых терминалов
    for elem in T:
        if elem not in n:
            f_n.append(elem)
    f_u=[] #Мн-во не достижимых не терминалов
    for elem in N:
        if elem not in u:
            f_u.append(elem)
    for elem in f_n:
        Pravila.pop(elem)

    if f_n!=[]:
        print(f'Недостижимые символы: {f_n} и {f_u}\nНовые правила:')
        return Pravila
    else: return f'Недостижимых символов нет'



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
P=DontGoSumb(P,TN)
print(P)
print(DontGenSumb(P,TN))