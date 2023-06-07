import gurobipy as gp
from gurobipy import GRB

# Dados do problema
n = 5  # número de clientes
Q = 3  # capacidade do veículo
c = [[0, 3, 1, 5, 8],
     [3, 0, 6, 7, 9],
     [1, 6, 0, 4, 2],
     [5, 7, 4, 0, 3],
     [8, 9, 2, 3, 0]]  # matriz de distâncias
d = [0, 1, 2, 3, 4]  # demandas dos clientes

# Modelo de programação linear inteira
m = gp.Model()

# Variáveis de decisão
x = m.addVars(n, n, vtype=GRB.BINARY, name='x')

# Função objetivo
m.setObjective(gp.quicksum(c[i][j] * x[i,j] for i in range(n) for j in range(n)), GRB.MINIMIZE)

# Restrições
m.addConstrs((gp.quicksum(x[i,j] for j in range(n)) == 1 for i in range(n)), name='origem_destino')
m.addConstrs((gp.quicksum(x[i,j] for i in range(n)) == 1 for j in range(n)), name='destino_origem')
m.addConstrs((gp.quicksum(d[i] * x[i,j] for i in range(n)) <= Q for j in range(1, n)), name='capacidade')
m.addConstrs((x[i,j] == 0 for i in range(n) for j in range(n) if i == j), name='diagonal')

# Executar otimização
m.optimize()

# Imprimir solução
if m.status == GRB.OPTIMAL:
    print('Custo total:', m.objVal)
    for i in range(n):
        for j in range(n):
            if x[i,j].x > 0:
                print('Rota %d -> %d: %d' % (i, j, x[i,j].x))
