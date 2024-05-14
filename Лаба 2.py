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
        if elem_t in Pravila.keys():
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
            for i in range(len(Prav)):
                if fin_el in Prav[i]:
                    Prav.pop()
            Pravila[key]=Prav
        Pravila.pop(fin_el)


    if t!=[]:
        print(f'\nНепорождающие нетерминалы: {t}\nНовые правила:')
        return Pravila
    else: return f'\nНепорождающих терминалов нет'

def DontGoSumb(Pravila:dict,TN:list,MB:bool):
    T=TN[0]
    N=TN[1]
    n=[TN[2]]
    u=[]
    for elem_n in n:
        if elem_n in Pravila.keys():
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

    if f_n!=[] and MB==True:
        print(f'\nНедостижимые символы: {f_n} и {f_u}\nНовые правила:')
        return Pravila
    elif f_n!=[] and MB==False:
        return Pravila
    else: return f'\nНедостижимых символов нет'

def DelERule(Pravila:dict,TN:list):
    T=TN[0]
    N=TN[1]
    E=[]
    u=0
    while u!=len(N):
        for key in Pravila.keys():
            for elem in Pravila[key]:
                for elem_elem in elem:
                    if (elem == 'e' or elem_elem in E) and key not in E:
                        E.append(key)
        u+=1
    
    for eel in E:
        temp=[]
        temp0=[] #Для замены в правилах
        temp.extend(Pravila[eel])
        if 'e' in temp:
            temp.remove('e')
            Pravila[eel] = temp

        for elem in temp:
            boole=[]
            pieces=[]
            for elel in elem:
                pieces.append(elel)
                if elel in T:
                    boole.append(True)
                else: boole.append(False)

            if False not in boole:
                continue

            tab=TableOfTruth(boole.count(False))
            for el in tab:
                temp_index=[]
                for b in range(len(boole)):
                    if boole[b]==False:
                        temp_index.append(b)
                
                pi2=[]
                pi2.extend(pieces)
                for i in range(len(temp_index)):
                    nword=''
                    if el[i]=='0':
                        pi2[temp_index[i]]='e'

                for p in pi2:
                    if p!='e':
                        nword+=p
                
                temp0.append(nword)

        for elem in temp0:
            if elem=='':
                temp0.pop(temp0.index(elem))                         
        
        if temp0!=[]:
            Pravila[eel]=temp0
      

    if E!=[]:
        print(f'\nНетерминалы с е-правилами: {E}\nНовые правила:')
        return Pravila
    else: return f'\nНетерминалов с e-правилами нет'

def TableOfTruth(num:int):
    tab=[]
    for kol in range(2**num):
        tab.append(list(bin(kol)[2:].zfill(num)))
    return tab

def UnitRules(Pravila:dict,TN:list):
    T=TN[0]
    N=TN[1]
    defect=[]
    for key in Pravila.keys():
        temp=[]
        for rule in Pravila[key]:
            if rule not in N:
                temp.append(rule)
            else:
                defect.append(rule)
                for another_rule in Pravila[rule]:
                    temp.append(another_rule)
        Pravila[key]=list(set(temp))
                
    if defect!=[]:
        print(f'\nНетерминалы с цепным правилом: {defect}\nНовые правила:')
        return Pravila
    else: return f'\nНетерминалов с цепным правилом нет'

def LeftFact(Pravila:dict):
    alph =["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    keys = list(Pravila)
    strs=[]
    for key in keys:
        temp_key=[]
        temp_nkey=[]
        for sumb in alph:
            if sumb not in Pravila.keys():
                break
        strr = None
        for rule1 in Pravila[key]:
            for rule2 in Pravila[key]:
                if rule1 != rule2 and len(rule1)>1 and len(rule2)>1:
                    count=0
                    for i1 in range(len(min(rule1, rule2))-1):
                        if rule1[i1] == rule2[i1]:
                            count+=1
                    if count>=1:
                        strr = rule2[:count]

        if strr!=None:
            strs.append(strr)
            count=len(strr)
            for rule in Pravila[key]:
                if strr in rule[:count]:
                    temp_nkey.append(rule[count:])
                else: temp_key.append(rule)
            temp_key.append(strr+sumb)
            Pravila[key]=temp_key
            Pravila[sumb]=temp_nkey
        
    if strs!=None:
        print(f'\nПовторяющиеся элементы: {strs}\nНовые правила:')
        return Pravila
    else: return f'\nПовторяющихся элементов нет'

def LeftRecursion(Pravila: dict):
    alph =["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    keys = list(Pravila)
    wrong=[]
    for key in keys:
        temp_key=[]
        temp_nkey=[]
        for sumb in alph:
            if sumb not in Pravila.keys():
                break
        for rule in Pravila[key]:
            if rule[0]==key:
                wrong.append(rule)
                temp_nkey.append(rule[1:]+sumb)
                temp_nkey.append(rule[1:])
                for rulei in Pravila[key]:
                    if rulei!=rule:
                        temp_key.append(rulei+sumb)
            else:
                temp_key.append(rule)
        if temp_nkey!=[]:
            Pravila[key]=temp_key
            Pravila[sumb]=temp_nkey
    if wrong!=[]:
        print(f'\nПравила с левой рекурсией: {wrong}\nНовые правила:')
        return Pravila
    else: return f'\nПравил с левой рекурсией нет'

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
print(DontGoSumb(P,TN,True))
TN=Grammar(P)
print(DelERule(P,TN))
print(DontGoSumb(P,TN,False))
TN=Grammar(P)
print(UnitRules(P,TN))
TN=Grammar(P)
print(LeftFact(P))
TN=Grammar(P)
print(LeftRecursion(P))
TN=Grammar(P)
print("\nФинальные правила имеют вид:")
for key in P.keys():
    print(f'{key} -> {P[key]}')

"""
X Y,Y=Y,Y<Y,Y>Y,K
Y Y^Z,Y#Z,e
Z na,nb,e
K nK
L l,a,b

"""