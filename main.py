import gurobipy as gp
from gurobipy import GRB

# Dados do problema
n = 5 # número de clientes
Q = 3 # capacidade do veículo
D = 10 # distancia máxima
d = [[0, 3, 1, 5, 8],
     [3, 0, 6, 7, 9],
     [1, 6, 0, 4, 2],
     [5, 7, 4, 0, 3],
     [8, 9, 2, 3, 0]]   # matriz de distâncias
q = [0, 1, 2, 3, 4]     # demandas dos clientes
k = 1 # numero de veiculos

# Modelo de programação linear inteira
m = gp.Model()

# Variáveis de decisão
x = m.addVars(n, n, vtype=GRB.BINARY, name='x')

# Função objetivo
m.setObjective(gp.quicksum(d[i][j] * x[i,j] for i in range(n) for j in range(n)), GRB.MINIMIZE)

# for i in range(1, n):
#     m.addConstr(gp.quicksum(x[i,j] for j in range(n)) == 1)  # Cada origem tem somente um destino
# for i in range(1, n):
#     m.addConstr(gp.quicksum(x[i,j] for j in range(n)) == 1)
#     m.addConstr(gp.quicksum(x[j,i] for j in range(n)) == 1)
#     m.addConstr(gp.quicksum(q[j] * x[i,j] for j in range(n)) <= Q)


# Restrições
m.addConstrs(gp.quicksum(x[i,j] for j in range(n)) == 1 for i in range(n)) # Cada origem tem somente um destino
m.addConstrs(gp.quicksum(x[i,j] for i in range(n)) == 1 for j in range(n))  # Cada destino tem somente uma origem
m.addConstrs(gp.quicksum(q[i] * x[i,j] for i in range(n)) <= Q for j in range(1, n)) # restrição de carga
m.addConstrs(gp.quicksum(d[i][j] * x[i,j] for j in range(n)) <= D for i in range(1, n)) # restrição de carga

m.addConstrs((x[i,j] == 0 for i in range(n) for j in range(n) if i == j)) # evitando pegar o ponto i = j


m.optimize()

# Imprimir solução
if m.status == GRB.OPTIMAL:
    print('Custo total:', m.objVal)
    for i in range(n):
        for j in range(n):
            # print('(i, j): (%d, %d): %d' % (i, j, x[i,j].x))
            if x[i,j].x > 0:
                print('Rota %d -> %d: %d' % (i, j, x[i,j].x))