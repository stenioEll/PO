#!/usr/bin/env python
# coding: utf-8

# In[206]:


import pandas as pd
import numpy as np
import ortools
from ortools.linear_solver import pywraplp
from ortools.graph import pywrapgraph


# In[207]:


#Abrindo o arquivo e salvando seus dados, linha a linha
arquivo = open("instancias/instance7.txt", 'r')
texto = arquivo.readlines()
arquivo.close()
print(texto)


# In[208]:


#Guardando dados nas variáveis
n_vertices = int(texto[0].split()[0])
n_arcos = int(texto[1].split()[0])
i_origem = int(texto[2].split()[0])
i_escoadouro = int(texto[3].split()[0])

pontoInicial = []
pontoFinal = []
capacidadeArco = []

for i in range(4, len(texto)):
    pontoInicial.append(int(texto[i].split()[0]))
    pontoFinal.append(int(texto[i].split()[1]))
    capacidadeArco.append(int(texto[i].split()[2]))

print(n_vertices, n_arcos, i_origem, i_escoadouro)
print(pontoInicial)
print(pontoFinal)
print(capacidadeArco)


# In[209]:


#transformando o problema de fluxo máximo em fluxo de custo mínimo

#definindo todos os custos como zero
custo = []
for i in range(4, len(texto)):
    custo.append(0)

#calculando o fluxo máximo viável
soma = 0
for i in capacidadeArco:
    soma += i

F = int(soma) #Limite do fluxo máximo viável pela rede
M = 900 #Custo unitário máximo
U = 10000 #Capacidade máxima de arco

pontoInicial.append(int(i_origem))
pontoFinal.append(int(i_escoadouro))
capacidadeArco.append(int(U))
custo.append(int(M))

#definindo as demandas em cada nó
suprimentos = []
for i in range(int(n_vertices)+1):
    suprimentos.append(0)

suprimentos[i_origem] = F
suprimentos[i_escoadouro] = -F

print(soma)
print(custo)
print(pontoInicial)
print(pontoFinal)
print(capacidadeArco)
print(custo)
print(suprimentos)


# In[210]:


fluxo_custo_min = pywrapgraph.SimpleMinCostFlow()
fluxo_max = 0

for i in range(0, len(pontoInicial)):
    fluxo_custo_min.AddArcWithCapacityAndUnitCost(pontoInicial[i], pontoFinal[i], capacidadeArco[i], custo[i])

for i in range(0, len(suprimentos)):
    fluxo_custo_min.SetNodeSupply(i, suprimentos[i])

if fluxo_custo_min.Solve() == fluxo_custo_min.OPTIMAL:
    print('Custo Mínimo:', fluxo_custo_min.OptimalCost())
    print('')
    print('  Arco    Fluxo / Capacidade  Custo')
    for i in range(fluxo_custo_min.NumArcs()):
        custoArco = fluxo_custo_min.Flow(i) * fluxo_custo_min.UnitCost(i)
        print('%1s -> %1s   %3s  / %3s       %3s' % (fluxo_custo_min.Tail(i), fluxo_custo_min.Head(i), fluxo_custo_min.Flow(i), fluxo_custo_min.Capacity(i), custoArco))
        
        #soma fluxo máximo
        if fluxo_custo_min.Tail(i) == 1 and fluxo_custo_min.Capacity(i) < U:
            fluxo_max += fluxo_custo_min.Flow(i)
else:
    print('Não foi possível encontrar a solução.')

print("")
print("Fluxo Máximo = ", fluxo_max)

