import random

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
    print(f'G = ( {N}, {T}, P, {S})')
    return [T,N]

def Iterations(Pravila:dict, itr):
    Fin_word='S' #Для вывода
    for_fun='S' #Для итераций
    i=0
    Pravila=Partition(Pravila)
    # while i<itr:
    #     ff=[]
    #     for el_ff in for_fun:
    #         ff.append(el_ff)
    #         for key in Pravila.keys():
    #             if key in for_fun:
    #                 indx=for_fun.index(key[0])
    #                 if for_fun[indx:indx+len(key)-1]==key[0:len(key)-1]:
    #                     for_fun=for_fun
    #                     for_fun[indx:indx+len(key)-1]=Pravila[key]
    #                     for_fun=''
    #                     for p in ff:
    #                         for_fun+=p
    #                     i+=1
    #             break



    #             if el_ff == key:
    #                 var=random.choice(Pravila.keys())
    #                 if type(var)!=str:
    #                     if itr%2==0:


    # while i<itr:
    #     for key in Pravila.keys():
    #         if key in for_fun:


    # while i<itr:
    #     for nom_el, el_f in enumerate(for_fun):
    #         for key in Pravila.keys():
    #             if el_f == key:
    #                 repl=random.choice(Pravila[key])
    #                 if type(repl)!=str:
    #                     u=Pravila[key]
    #                     if itr%2==0:
    #                         if i==itr:
    #                             repl=random.choice(u[1])
    #                         else:
    #                             repl=random.choice(u[0])
    #                     else:
    #                         if i==itr-1:
    #                             repl=random.choice(u[1])
    #                         else:
    #                             repl=random.choice(u[0])
    #                 for_fun=for_fun.replace(for_fun[nom_el],repl)
    #                 if for_fun[-2:]=='bB' or for_fun[-2:]=='dB':
    #                     i+=1
    #                     continue
    #                 else: Fin_word+= f' -> {for_fun}'
    #                 i+=1
    # return Fin_word

def Partition(Pravila:dict):
    for key in Pravila.keys():
        right=[]
        left=[]
        end=[]
        if len(Pravila[key])>=2:
            for i in Pravila[key]:
                if str(i).isupper():
                    right.append(i)
                else:
                    left.append(i)
            if len(right)==0 or len(left)==0:
                continue
            else:
                end.append(right)
                end.append(left)
                Pravila[key]=end
    return Pravila

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

P={}
u=True
print('Введите правила:')
while u==True:
    try:
        key, prav=input().split()
        P[key]=prav.split(',')
    except:
        u=False
print('Правила: \n',P)
print('Грамматика: ')
TN=Grammar(P)
print('Проверка типа: ',Check(P,TN))
itr=int(input('Введите количество итераций: '))*2
print(Iterations(P,itr))