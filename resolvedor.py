from pyparsing import And
import entrada_o
import math
import numpy as np
import copy
import sys
from pickle import LIST
from pandas import DataFrame as pd
from pandas import ExcelWriter as ex
import streamlit as st


class Pos():
    def __init__(self):
        self.produto = 0
        self.quantidade = 0       
class SA():
    def __init__(self):
        self.cestas= self.Cesta()
        self.car=self.Carro()
        self.x=0
        self.y=0
        self.x0=0
        self.y0=0
        #self.alpha = 0.95
        #self.iter=10
        #self.Tf = 1.0
        #self.T0 = 5.0
        self.arm= entrada_o.Armazem()
        #self.cel=[]
        self.SOL=[]
        self.Xb=[]
        self.xb=[]
        self.xxb = sys.maxsize
        self.xy = [0,0]
        self.order=[]
        self.pos_ordem=[]
        self.maxcar=2
    class Carro:
        def __init__(self):
            self.capcesta=10
            self.numcestas=8
            self.captotal=self.capcesta*self.numcestas
            self.carrinho=[]
    class Cesta:
        def __init__(self):
            self.produtos=[]
            self.ordem=0

    def arquivos(self):
        file=open('entrada.txt','r')
        arq = file.read().splitlines()
        try:
            filepath1=arq[0]
            filepath2=arq[1]
            filepath3=arq[2]

            file1 = open(filepath1, 'r')
            arq1 = file1.read().splitlines()

            file2 = open(filepath2, 'r')
            arq2 = file2.read().splitlines()

            file3 = open(filepath3, 'r')
            arq3 = file3.read().splitlines()

            self.arm.leitura(arq1,arq2,arq3)
        except:
            self.arm.openFile()

    def solInicial(self):
        self.SOL=[]
        self.order=[]
        self.pos_ordem=[]
        for i in range(self.arm.totalord):
            self.pos_ordem.append(-1)
        for i in range(self.car.numcestas):
                self.car.carrinho.append(self.cestas)
        self.SOL=[]

        self.randomid1 = []
        for j in range(len(self.arm.loc)):
            for k in range(len(self.arm.loc[j])):
                self.randomid1.append((j+1,k+1))
        np.random.shuffle(self.randomid1)
        for i in range(self.arm.totalpro):
            self.SOL.append(self.randomid1[i])
        self.order=copy.deepcopy(self.arm.ordens)
       
    def imprimeSol(self,SOL,order):


        print('Layout solu????o: ',SOL)
        print('Lista de produtos: ',order)
    def imprimeOrd(self,order):
        print('Lista de produtos: ',order)

    def organizar(self,order):

        for i in range(len(order)):
            o,p,u=order[i]
            for j in range(i+1,len(order)):
                k,s,v=order[j]
                if o==k:
                    aux=order[j]
                    order.pop(j)
                    order.insert(i+1,aux)
                    


    def objetivo(self,SOL,ordem):
        order=copy.deepcopy(ordem)
        '''
        print("Ordem antes",order)
        
        print("Ordem depois",order)
        '''
        #order: (produto,ordem)
        #SOL: {Produto: (n??,prateleira)}s
        for i in range(len(self.pos_ordem)):
            self.pos_ordem[i]=-1
        objetivo=[]
        objt=0.0
        cesta_usada=0
        #Coleta primeiro produto
        i,j,e=order[0]
        a,b=SOL[i-1]
        capcar=0
        objt += self.arm.dist[0][a]
        self.pos_ordem[j]=cesta_usada
        cesta_usada+=1
        self.car.carrinho[self.pos_ordem[j]].produtos.append(i)
        capcar+=1
        l=0
        while len(order)!=1:
            o,p,u=order[l]
            a,b=self.SOL[o-1]
            if self.pos_ordem[p] != -1:
                u=self.pos_ordem[p]
            else:
                self.pos_ordem[p]=cesta_usada
                cesta_usada+=1
            k,s,v=order[l+1]
            c,d=SOL[k-1]

            if self.pos_ordem[s] != -1:
                v=self.pos_ordem[s]
            else:
                self.pos_ordem[s]=cesta_usada
                cesta_usada+=1

            if cesta_usada>=self.car.capcesta:
                objt += self.arm.dist[a][0]
                for i in range(len(self.car.carrinho)):
                    self.car.carrinho[i].produtos=[]
                objt += self.arm.dist[0][c]

                self.car.carrinho[v].produtos.append(c)
                for j in range(len(self.pos_ordem)):
                    self.pos_ordem[j]=-1
                cesta_usada=0
                self.pos_ordem[s]=cesta_usada
                cesta_usada+=1
                capcar+=1
                order.pop(l)  
            else:
                objt += self.arm.dist[a][c]
                self.car.carrinho[v].produtos.append(c)
                capcar+=1
                order.pop(l) 
                
        #Retorna para a entrada
        i=len(order)-1
        g,h,v=order[i]
        a,b=SOL[h-1]
            
        objt += self.arm.dist[a][0]

            
        objetivo.append(objt)

        return sum(objetivo)

    
    def sa(self,order):
        #self.rd = np.random.randint(0,2)
        self.arm.openFile(order)
        
        self.alpha =0.8
        self.it = 5
        self.Tf = 1
        self.T0 = 5
        #self.arquivos()
        del self.SOL
        del self.order
        self.SOL=[]
        self.order=[]
        self.pos_ordem=[]
        self.solInicial()
        #self.imprimeSol(self.SOL,self.order)
        valor=self.objetivo(self.SOL,self.order)
 
        self.organizar(self.order)

        st.write("Initial Cost:", valor)
        #print("Custo inicial:", valor)
        
        self.Xb = copy.deepcopy(self.SOL)
        self.orderB=copy.deepcopy(self.order)
        self.xxb=valor

        self.T = self.T0

        while self.T >= self.Tf:
            for i in range(self.it):
                #print('-----------------ITERA????O------------------')
                xx,ord = self.SA2(self.SOL,self.order)
                Y = copy.deepcopy(self.SOL)
                
                rd = np.random.randint(0,1)
                # self.r = self.rd
                if rd == 0:
                    self.N1(Y)
                   
                elif rd == 1:
                    self.N2(Y)
                   
                elif rd == 2:
                    self.N3(Y)
                  
                yy,ordy = self.SA2(Y,ord)
                delta = yy-xx
                if delta <= 0:
                    self.SOL = copy.deepcopy(Y)
                    self.order=copy.deepcopy(ordy)
                    # self.SOL = self.Y
                    xx = yy
                else:
                    rr = (np.random.randint(0,100))/100
                    if rr < math.exp(-delta/self.T):
                        # self.SOL = self.Y
                        self.SOL = copy.deepcopy(Y)
                        self.order=copy.deepcopy(ordy)
                        xx = yy
                if xx < self.xxb:
                    # self.Xb = self.SOL
                    self.Xb = copy.deepcopy(self.SOL)
                    self.orderB=copy.deepcopy(self.order)
                    self.xxb = xx
            
            self.T=self.alpha*self.T
            #print("-Temperatura Atual:",self.T)
        #self.imprimeSol(self.Xb,self.orderB)
        st.write("-Total cost of solution:",self.xxb)
        #print("-Custo Total da solu????o:",self.xxb)
        #self.datatxt(self.xxb,self.Xb,self.orderB)
        self.save_xls
        return self.xxb

    def N1(self, SOL):
        # self.SOL = SOL
        i = np.random.randint(0,len(SOL)-1)
        
        j = np.random.randint(0,len(SOL)-1)

        cont =5
        while i == j and cont >=0:
            i = np.random.randint(0,len(SOL)-1)
            j = np.random.randint(0,len(SOL)-1)
            cont= cont-1
        
        aux = SOL[i]
        SOL[i]= SOL[j]
        SOL[j]= aux
        
        #print("N1")
    def N2(self,SOL):
        # self.SOL = SOL
        i = np.random.randint(0,len(SOL)-1)

        j = np.random.randint(0,len(SOL)-1)

        cont=5
        while i == j and cont >=0:
            i = np.random.randint(0,len(SOL)-1)

            j = np.random.randint(0,len(SOL)-1)
            cont=cont-1
        aux=SOL[i]
        SOL.pop(i)
        SOL.insert(j,aux)
        
        #self.SOL[self.j][self.jc].quantidade = 0
        #print("N2")
    def N3(self,SOL):
        # self.SOL = SOL
        i = np.random.randint(0,len(SOL))
        j =0
        A0= sys.maxsize

        if SOL[i] == 0:
            return
        k=i
        for l in range(self.arm.cel):
            A = self.dist(self.arm.nex, self.arm.ney, self.arm.pa[k].pra[l].xcel,self.arm.pa[k].pra[l].ycel)
            if SOL[k][l] == 0 and A < A0:
                A0 = A
                j = k
                jc = l
        # if self.SOL[self.j][self.jc] != 0:
        #     return
        # if self.SOL[self.j][self.jc] != 0 and self.SOL[self.i][self.ic] == 0:
        #     return
        SOL[j] = SOL[i]
        SOL[i]= 0

        #self.SOL[self.i][self.ic].quantidade = 0
        #print("N3")
    def SA2(self,arm,ord):
        alpha =0.8
        it = 5
        Tf = 1
        T0 = 5
        T=T0
        xxb=sys.maxsize
        while T >= Tf:
            for i in range(it):
                xx = self.objetivo(arm,ord)
                y = copy.deepcopy(ord)
                rd = np.random.randint(0,1)
                # self.r = self.rd
                if rd == 0:
                    self.N_1(y)
                   
                elif rd == 1:
                    self.N_2(y)
                   
                self.organizar(y)
                yy = self.objetivo(arm,y)
                #print('yy: ',yy)
                delta = yy-xx
                if delta <= 0:
                    ord= copy.deepcopy(y)
                    # self.SOL = self.Y
                    xx = yy
                else:
                    rr = (np.random.randint(0,100))/100
                    if rr < math.exp(-delta/T):
                        # self.SOL = self.Y
                        ord = copy.deepcopy(y)
                        xx = yy
                if xx < xxb:
                    # self.Xb = self.SOL
                    xb = copy.deepcopy(ord)
                    xxb = xx
            
            T=alpha*T
            #print("-Temperatura Atual:",self.T)
        '''
        print("-Solu????o do SA2:")
        
        '''
        
        #self.imprimeSol(arm,xb)
        #print("-Custo solu????o SA2:",xxb)
        
        return xxb,xb
    def N_1(self,order):

        ii = np.random.randint(0,len(order)-1)
        jj = np.random.randint(0,len(order)-1)
        cont=5
        while ii==jj and cont >=0:
            ii = np.random.randint(0,len(order)-1)
            jj = np.random.randint(0,len(order)-1)
            cont=cont-1
        #print(ii,jj)
        aux = order[ii]
        order[ii]= order[jj]
        order[jj]= aux

    def N_2(self,order):

        ii = np.random.randint(0,len(order)-1)
        jj = np.random.randint(0,len(order)-1)
        cont=5
        while ii==jj and cont >=0:
            ii = np.random.randint(0,len(order)-1)
            jj = np.random.randint(0,len(order)-1)
            cont=cont-1
        #print(ii,jj)
        aux = order[ii]
        order.pop(order[ii])
        order.insert(order[jj],aux)
    
    def save_xls(self):
        produtos=np.arange(1,len(self.Xb)+1)

        nos=[]
        prateleira=[]
        for j in range(len(self.Xb)):
            a,b=self.Xb[j]
            nos.append(a)
            prateleira.append(b)
        produto_o=[]
        ordem=[]
        for i in range(len(self.orderB)):
            print(b)
            a,b,c=self.orderB[i]
            produto_o.append(a)
            #ordem.append(b)
        df1 = pd({'Products': produto_o,'Order': ordem})
        df2 = pd({'Products': produtos,'Nodes': nos,'Shelves': prateleira})

        # Usando o ExcelWriter, cria um doc .xlsx, usando engine='xlsxwriter'
        #writer = ex('Solution.xlsx')
        #writer = ex('Solution.xlsx', engine='xlsxwriter')

        # Armazena cada df em uma planilha diferente do mesmo arquivo
        df1.to_csv('orders.csv')
        df2.to_csv('layout.csv')

        # Fecha o ExcelWriter e gera o arquivo .xlsx
        print("Solucao salva!")