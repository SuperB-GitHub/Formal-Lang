from matplotlib import pyplot as plt
from prettytable import PrettyTable
import networkx as nx

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
    print(f'\nНовые правила после добавления N:')
    return Pravila

def FuncTransit(Pravila:dict, N:str ,T:str):
    ans=[]
    if N == "N":return "Ø"
    else:
        for rule in Pravila[N]:
            if rule[0] == T and len(rule)==2:
                ans.append(rule[1:])
        if ans==[]: return "Ø"
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
            row_names.append(FuncTransit(Pravila,column,row))
        table.add_row(row_names)
    return table    

def NotDetermGraph(Pravila:dict,TN: list):
    G=nx.DiGraph()
    T = TN[0]
    N = TN[1]
    edge_labels={}
    for depart in N:
        for edge in T:
            arrival = FuncTransit(Pravila,depart,edge)
            if type(arrival)==list:
                for el in arrival:
                    edge_labels[(depart,el)]=edge
    G.add_edges_from(edge_labels.keys())
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels = True)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_color="blue")
    plt.show()
            
def Parameters(Pravila:dict, TN:list): 
    Q = TN[1] 
    T = TN[0]
    F = TableFuncTrasnsit(Pravila,TN) 
    H = TN[2]
    Z = []
    for notterm in Q:
        check=[]
        for term in T:
            check.append(FuncTransit(Pravila,notterm,term))
        if check.count("Ø") == len(check):
            Z.append(notterm)
    if "e" in Pravila[H]:
        Z.append(H)
    print(f"""\nКонечный автомат M:\nQ = {Q} - Мн-во состояний автомата\nT = {T} - Мн-во входного алф\nF - Таблица функции переходов\n{F}\nH = {H} - Начальное состояние\nZ = {Z} - Мн-во заключительных состояний\n""")
    return [Q,T,F,H,Z]

def DictDKA(Pravila:dict,TN: list):
    alph =["A","B","C","D","E","I","J","K","L","M","N","O","P","R","S","U","V","W","X","Y"]
    T = TN[0]
    N = TN[1]
    dka={}
    columns = []
    columns.extend(N)
    for column in columns:
        column_names = []
        for row in T:

            #Сортировка если парное значение column
            if len(column)>1:
                el_names = [] #Значения отправляющиеся в словарь
                for el in column:
                    ft = FuncTransit(Pravila,el,row)

                    #Добавление если с функции парное значение
                    if len(ft)>1:
                        for el_ft in ft:
                            if el_ft not in el_names:
                                el_names.append(el_ft)
                    #Добавление если единичное значение
                    elif ft[0] not in el_names:
                        el_names.append(ft[0])
                
                #Отправление в словарный лист если парное значение
                if len(el_names)>1: column_names.append(el_names)

                #Отправление в словарный лист если одно значение
                elif len(el_names)==1 and type(el_names[0])==list: column_names.append(el_names[0])

                #Отправление в словарный лист если пустое мн и др.
                else: column_names.append("".join(el_names))

                #Отправление в columns для след разборов
                if tuple(el_names) not in columns and "Ø" not in el_names:
                    columns.append(tuple(el_names))

            #Сортировка если единичное значение column
            else:       
                ft = FuncTransit(Pravila,column,row)

                #Добавление если с функции парное значение
                if len(ft)>1:
                    column_names.append(ft) #В словарь
                    columns.append(tuple(ft)) #Для след разборов

                #Добавление если единичное значение
                else:
                    ft = "".join(ft)
                    column_names.append(ft) #В словарь
                    if ft not in columns and ft!="Ø":  
                        columns.append(tuple(ft)) #Для след разбора
        
        #Внесение в словарь
        dka[column]=column_names

    #Создание словаря для замены
    keys = list(dka)
    zamena = {}
    for key in keys:
        for sumb in alph:
            if sumb not in zamena.values() and sumb not in dka.keys():
                break
        if len(key)>1:
            zamena[key]=sumb

    #Замена двусоставных правил
    for key in keys:
        temp=[]
        for rule in dka[key]:
            if type(rule)==list: #Замена в правилах
                if "Ø" in rule:
                    rule.pop(rule.index("Ø"))
                    temp.append("".join(rule))
                else:
                    temp.append(zamena[tuple(rule)])
            else: temp.append(rule)
        dka[key]=temp
        if type(key) == tuple: #Замена в ключах
            dka[zamena[key]]=dka[key]
            del dka[key]
    
    zam = ""
    for key in zamena.keys(): zam += f"{key} -> {zamena[key]}; "
    print(f"Правила ДКА:\nЗамена: {zam}\nПри входных символах:\nT -> {T}")
    for key in dka.keys(): print(f'{key} -> {dka[key]}')

    return dka

def DKAGraph(dka:dict,M:list):
    G=nx.DiGraph()
    edge_labels={}
    for depart in dka.keys():
        for num_edge, arrival in enumerate(dka[depart]):
            if arrival != "Ø":
                edge_labels[(depart,arrival)]=M[1][num_edge]
    G.add_edges_from(edge_labels.keys())
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels = True)
    nx.draw_networkx_edge_labels(G,pos,edge_labels,font_color="blue")
    plt.show()


    


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
M=Parameters(P,TN)
NotDetermGraph(P,TN)
DKA = DictDKA(P,TN)
DKAGraph(DKA,M)



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