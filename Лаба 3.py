from prettytable import PrettyTable

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
            if key in N and ((el[-1] in N and el[0] in T)  or (el[0] in N and el[-1] in T)):
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

def AddNewN(Pravila: dict,TN: list):
    T=TN[0]
    N=TN[1]
    for key in Pravila.keys():
        temp_key = []
        for rule in Pravila[key]:
            if rule in T:
                temp_key.append(rule+"N")
            temp_key.append(rule)
        Pravila[key]=temp_key
    print(f'\nНовые правила:')
    return Pravila

def FuncTransit(Pravila:dict, N:str ,T:str):
    ans=[]
    for rule in Pravila[N]:
        if rule[0] == T and len(rule)==2:
            ans.append(rule[1:])
    if ans==[]:
        return "Ø"
    else: return ans

def TableFuncTrasnsit(Pravila:dict,TN: list):
    T = TN[0]
    N = TN[1]
    table=PrettyTable()
    field_names = ["F"]
    for fn in N:
        field_names.append(fn)
    table.field_names = field_names
    for row in T:
        row_names = [row]
        for column in N:
            if column == "N":
                row_names.append("Ø")
            else:
                row_names.append(FuncTransit(Pravila,column,row))
        table.add_row(row_names)
    return table    

# def




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
print(AddNewN(P,TN))
TN=Grammar(P)
print(f"\nТаблица функции переходов:\n{TableFuncTrasnsit(P,TN)}\n")



"""
S aA,bB
A cC,#
C cC,cA
B dD,#
D dD,dB

S aB,aA
B bB,a
A aA,b

"""