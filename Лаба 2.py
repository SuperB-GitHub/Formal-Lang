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
    typ=[]

    for key in Pravila.keys():
        for el in Pravila[key]:
            if key in N and ((el[-1] in T and el[0] in N)  or (el[0] in T and el[-1] in N)):
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
        for el in Pravila[key]:
            if any(symb in el for symb in N)!=True:
                return f'не существует в правиле {key} в месте {el}'



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