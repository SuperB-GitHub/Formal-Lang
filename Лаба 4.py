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

def FuncTransit(Pravila:dict, N:str ,T:str):
    ans=[]
    try:
        for rule in Pravila[N]:
            if rule[0] == T and len(rule)==2:
                ans.append(rule[1:])
    finally:
        if ans==[]: return "Ø"
        else: return ans

def TableFuncTrasnsit(Pravila:dict,TN: list):
    T = TN[0]
    N = TN[1]
    table=PrettyTable()
    field_names = ["f"]
    for fn in N:
        field_names.append(fn)
    table.field_names = field_names
    for row in T:
        row_names = [row]
        for column in N:
            row_names.append(FuncTransit(Pravila,column,row))
        table.add_row(row_names)
    return table

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

def FirstGraph(Pravila:dict,TN:list):
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

def DontGoSumb(Pravila:dict,TN:list):
    T=TN[0]
    N=TN[1]
    n=[TN[2]]
    for elem_n in n:
        if elem_n in Pravila.keys():
            for elem in Pravila[elem_n]:
                for elem_in_elem in elem:
                    if elem_in_elem not in n and elem_in_elem in N:
                        n.append(elem_in_elem)
    f_n=[] #Мн-во не достижимых терминалов
    for elem in N:
        if elem not in n:
            f_n.append(elem)
    for elem in f_n:
        Pravila.pop(elem)

    if f_n!=[]:
        print(f'\nНедостижимые символы: {f_n}\nНовые правила:')
        return Pravila
    else: return f'\nНедостижимых символов нет'

def ChangeSost(Pravila:dict,r:list):
    for sost_s in r:
        if len(sost_s)>2:
            for key1_i in range(len(sost_s)):
                new = []
                rule1 = Pravila[sost_s[key1_i]]
                for key2_i in range(len(sost_s)):
                    rule2 = Pravila[sost_s[key2_i]]
                    if len(rule1)==1 and len(rule2)==1:
                        rule1str = "".join(rule1)
                        rule2str = "".join(rule2)
                        if key1_i!=key2_i and rule1str[:1]==rule2str[:1]:
                            for rs in r:
                                if rule1str[1:] in rs and rule2str[1:] in rs:
                                    new.append(sost_s[key1_i])
                                    new.append(sost_s[key2_i])
                                    for key in new:
                                        sost_s.remove(key)
                                    if new not in r:
                                        r.insert(1,new)
                                    return r
                new.append(sost_s[key1_i])
                sost_s.remove(sost_s[key1_i])
                if new not in r:
                    r.insert(1,new)
                return r

def CombEqival(Pravila:dict,TN:list,M:list):
    print("\nОбъединение эквивалентных состояний:")
    Q = []
    Q.extend(TN[1])
    Q.remove(''.join(M[4]))
    R = [Q, M[4]]
    print(f"R{0} = {R}")
    b = True
    count = 1
    while b == True:
        r = R.copy()
        ChangeSost(Pravila,R)
        if r==R:
            b = False
        else:
            r = R.copy()
            print(f"R{count} = {R}")
            count += 1
    return R

def MakePravAgain(Pravila:dict, R:list):
    alph =["A","B","C","D","E","I","J","K","L","M","N","O","P","R","S","U","V","W","X","Y"]
    zamena = {}
    for count, sost in enumerate(R):
        if len(sost) == 1:
            R[count] = ''.join(sost)
        else:
            for sumb in alph:
                if sumb not in Pravila.keys() and sumb not in zamena.values():
                    break
            for sost_i in sost:
                zamena[sost_i] = sumb
            R[count] = sumb
    print(f"\nПри {zamena} эквив состояния принимают след вид:\nRi = {R}")
    keys = list(Pravila)
    for key in keys:
        if key not in R and zamena[key] not in Pravila.keys():
            Pravila[zamena[key]] = Pravila[key]
            del Pravila[key]
        elif key not in R and zamena[key] in Pravila.keys():
            Pravila[zamena[key]].append(''.join(Pravila[key]))
            del Pravila[key]
    for key in Pravila.keys():
        new = []
        for value_prav in Pravila[key]:
            if value_prav[1:] in zamena.keys():
                new_zn = value_prav.replace(value_prav[1:],zamena[value_prav[1:]])
                if new_zn not in new:
                    new.append(new_zn)
            else:
                if value_prav not in new:
                    new.append(value_prav)
        Pravila[key] = new

    
    print(f"\nНовые правила:")
    return Pravila

        



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
TN = Grammar(P)
M = Parameters(P,TN)
FirstGraph(P,TN)
print(DontGoSumb(P,TN))
TN = Grammar(P)
R = CombEqival(P,TN,M)
print(MakePravAgain(P,R))
TN = Grammar(P)
FirstGraph(P,TN)



"""
S (M
K 1M
L 0K
M 1R,0R
N 1M
O 0N
Q 0R
T 1Q,)U
R #L,)U,~O
P 1R
F 0P,)U

"""