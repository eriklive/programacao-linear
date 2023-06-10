import gurobipy as gp
from gurobipy import GRB

rotas: list = []

# Dados do problema
n: int = 5 # número de clientes
Q: int = 13 # capacidade do veículo
q: list = [0, 4, 3, 3, 2]     # demandas dos clientes
D: int = 10 # distancia máxima
d: list = [
        [0, 3, 1, 5, 8],
        [3, 0, 6, 7, 11],
        [1, 6, 0, 4, 2],
        [5, 7, 4, 0, 3],
        [8, 11, 2, 3, 0]
    ]   # matriz de distâncias
k: int = 1 # número de veículos
ORIGEM = 1


def logarCargaDaViagem(destinos, listaDeCargas):
    cargaDaViagem: int = 0

    for elemento in range(0, destinos):
        cargaDaViagem += listaDeCargas[elemento]
    
    print('Carga da viagem: %d, limite: %d' % (cargaDaViagem, Q))   

def acharRotaOtima(n: int, d: list, q: list, Q: int, D: int):
    modelo = gp.Model()

    x = modelo.addVars(n, n, vtype=GRB.BINARY, name='x')
    u = modelo.addVars(n, vtype=GRB.INTEGER, name='u')

    funcaoObjetivo = gp.quicksum(d[i][j] * x[i,j] for i in range(n) for j in range(n))

    modelo.setObjective(funcaoObjetivo, GRB.MINIMIZE) # Kara 1

    modelo.addConstr(gp.quicksum(x[0,i] for i in range(1, n)) == 1) # Kara 4
    modelo.addConstr(gp.quicksum(x[i,0] for i in range(1, n)) == 1) # Kara 5
    
    
    for i in range(1, n):    
        modelo.addConstr(gp.quicksum(x[i,j] for j in range(n)) == 1) # Kara 3
        modelo.addConstr(gp.quicksum(q[j] * x[i,j] for j in range(n)) <= Q) # NADA
        modelo.addConstr(gp.quicksum(d[i][j] * x[i,j] for j in range(n)) <= D) # NADA

        for j in range(1, n): # Kara Apendices
            if q[i] + q[j] > Q:
                modelo.addConstr(x[i,j] == 0  )
            if i == j:
                modelo.addConstr(x[i,j] == 0 )

    for j in range(1, n):    
        modelo.addConstr(gp.quicksum(x[i,j] for i in range(n)) == 1) # Kara 2

    for i in range(1, n):    
        modelo.addConstr(u[i] - gp.quicksum(q[j] * x[j,i] for j in range(2, n) if j != i) >= q[i] ) # Kara 9
        modelo.addConstr(u[i] + (Q - q[i]) * x[1,i] <= Q) # Kara 10
        for j in range(1, n):  
            if(i != j):
                modelo.addConstr(u[i] - u[j] + Q * x[i, j] + (Q - q[i] - q[j]) * x[j,i] <= Q - q[j] ) # Kara 11

    modelo.optimize()
    
    # # Imprimir solução
    if modelo.status == GRB.OPTIMAL:
        print('distancia:', modelo.objVal)
        logarCargaDaViagem(n, q)

        for i in range(n):
            print('=========')
            print('u: %i' % ( u[i].x))

            for j in range(n):
                if x[i,j].x > 0:
                    print('Sub-rota %d -> %d' % (i, j))

acharRotaOtima(n, d, q, Q, D)
