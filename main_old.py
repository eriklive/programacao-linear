import gurobipy as gp
from gurobipy import GRB

rotas: list = []

# Dados do problema
n: int = 5 # número de clientes
Q: int = 3 # capacidade do veículo
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
    funcaoObjetivo = gp.quicksum(d[i][j] * x[i,j] for i in range(n) for j in range(n))

    modelo.params.LogToConsole = 0 # Comentar essa linha para retornar logs do Gurobi
    modelo.setObjective(funcaoObjetivo, GRB.MINIMIZE)

    for i in range(1, n):    
        modelo.addConstr(gp.quicksum(x[i,j] for j in range(n)) == 1)
        modelo.addConstr(gp.quicksum(x[j,i] for j in range(n)) == 1)
        modelo.addConstr(gp.quicksum(q[j] * x[i,j] for j in range(n)) <= Q)
        modelo.addConstr(gp.quicksum(d[i][j] * x[i,j] for j in range(n)) <= D)

    modelo.addConstr(gp.quicksum(x[0,j] for j in range(n)) == 1)
    modelo.addConstr(gp.quicksum(x[j,0] for j in range(n)) == 1)

    modelo.addConstrs((x[i,j] == 0 for i in range(n) for j in range(n) if i == j)) 
    # modelo.addConstrs(gp.quicksum(d[i][j] * x[i,j] for i in range(n) for j in range(n)) <= D) 
    
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
                    print('Sub-rota %d -> %d: %d' % (i, j, x[i,j].x))

    print('=============================')

# def iterador(clientes: int, iteracao: int, d: list, q: list, Q: int, D: int):
#     if(iteracao >= n):
#         return

#     try:
#         distanciasInternas: list = []
#         cargasInternas: list = []

#         for cliente in range(0, clientes):
#             distanciasInternas.append(d[cliente])
#             cargasInternas.append(q[cliente])

#         print(distanciasInternas)
#         acharRotaOtima(clientes, distanciasInternas, cargasInternas, Q, D)
#     except:
#         # Quando dá erro, é sinal que "estourou", então calculo as rotas até o cliente anterior
#         print('erro ao achar rota otima')
#         rotas.append(acharRotaOtima(clientes - 1, d, q, Q, D))
#         d = d[:clientes - 1]

#     iterador(clientes + 1, iteracao + 1, d, q, Q, D)
acharRotaOtima(n, d, q, Q, D)

# iterador(1,0, d, q, Q, D)

# if len(rotas) == 0:
#     rotas.append(acharRotaOtima(n, d, q, Q, D))


print('rotas: %d' % len(rotas))

# for i in range(n):
#     for j in range(n):
#         if x[i,j].x > 0:
#             print('Rota %d -> %d: %d' % (i, j, x[i,j].x))

# for i in range(1, n):
#     m.addConstr(gp.quicksum(x[i,j] for j in range(n)) == 1)  # Cada origem tem somente um destino
# for i in range(1, n):
#     m.addConstr(gp.quicksum(x[i,j] for j in range(n)) == 1)
#     m.addConstr(gp.quicksum(x[j,i] for j in range(n)) == 1)
#     m.addConstr(gp.quicksum(q[j] * x[i,j] for j in range(n)) <= Q)

# for cliente in range(1, n + 1):
#     try:
#         distanciasInternas = []
#         cargasInternas = []

#         for i in range(0, cliente):
#             distanciasInternas.append(d[i])
#             cargasInternas.append(q[i])

#         print(distanciasInternas)
#         acharRotaOtima(cliente, distanciasInternas, cargasInternas, Q, D)
#     except:
#         print('erro ao achar rota otima')
#         rotas.append(acharRotaOtima(cliente - 1, d, q, Q, D))