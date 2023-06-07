import gurobipy as gp
from gurobipy import GRB

rotas: list = []

# Dados do problema
n: int = 5 # número de clientes
Q: int = 8 # capacidade do veículo
q: list = [0, 1, 2, 3, 4]     # demandas dos clientes
D: int = 9 # distancia máxima
d: list = [
        [0, 3, 1, 5, 8],
        [3, 0, 6, 7, 11],
        [1, 6, 0, 4, 2],
        [5, 7, 4, 0, 3],
        [8, 11, 2, 3, 0]
    ]   # matriz de distâncias


def logarCargaDaViagem(destinos, listaDeCargas):
    cargaDaViagem: int = 0

    for elemento in range(0, destinos):
        cargaDaViagem += listaDeCargas[elemento]
    
    print('Carga da viagem: %d, limite: %d' % (cargaDaViagem, Q))   

def acharRotaOtima(n: int, d: list, q: list, Q: int, D: int):
    # Definição do modelo
    modelo = gp.Model()

    x = modelo.addVars(n, n, vtype=GRB.BINARY, name='x')
    u = modelo.addVars(n, vtype=GRB.INTEGER, name='u')

    funcaoObjetivo = gp.quicksum(d[i][j] * x[i,j] for i in range(n) for j in range(n))

    # modelo.params.LogToConsole = 0 # Comentar essa linha para retornar logs do Gurobi
    modelo.setObjective(funcaoObjetivo, GRB.MINIMIZE)

    for i in range(1, n):    
        modelo.addConstr(gp.quicksum(x[i,j] for j in range(n)) == 1)
        modelo.addConstr(gp.quicksum(x[j,i] for j in range(n)) == 1)
        modelo.addConstr(gp.quicksum(q[j] * x[i,j] for j in range(n)) <= Q)
        modelo.addConstr(gp.quicksum(d[i][j] * x[i,j] for j in range(n)) <= D)
    for i in range(2, n):    
        modelo.addConstr(u[i] - gp.quicksum(q[j] * x[j,i] for j in range(2, n)) >= q[i]) # restrição de carga (inferior)
        modelo.addConstr(u[i] + (Q - q[i]) * x[1,i] <= Q) # restricao de carga (superior)
        for j in range(2, n):
            modelo.addConstr(u[i] - u[j] + Q * x[i, j] + (Q - q[i] - q[j]) * x[j,i] <= Q - q[j] ) # Prevenção de sub-rotas

    modelo.addConstr(gp.quicksum(x[0,j] for j in range(n)) == 1)
    modelo.addConstr(gp.quicksum(x[j,0] for j in range(n)) == 1)
    

    modelo.addConstrs(x[i,j] == 0 for i in range(n) for j in range(n) if i == j)
    
    # ===========================================================================================================
    # Programa está solenemente ignorando essa restrição
    # modelo.addConstrs(restricaoDeCarga) # restrição de carga
    # ===========================================================================================================


    modelo.optimize()
    
    # # Imprimir solução
    if modelo.status == GRB.OPTIMAL:
        print('distancia:', modelo.objVal)
        logarCargaDaViagem(n, q)

        for i in range(n):
            for j in range(n):
                if x[i,j].x > 0:
                    print('Sub-rota %d -> %d' % (i, j))
                    print('x: %d' % ( x[i,j].x))
                    print('u: %i' % ( u[i].x))

acharRotaOtima(n, d, q, Q, D)
