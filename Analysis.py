import statistics as stats

f = open('Results.txt', 'r')
raw_data = f.read().split("\n")
f.close()

results = list()

for line in raw_data:
    if line.strip():
        results.append(float(line.split(',')[-1]))

print("Pior resultado: ", max(results))
print("Melhor resultado: ", min(results))
print("Média dos resultados: %.4f" % stats.mean(results))
print("Mediana dos resultados: %.4f" % stats.median(results))
print("Moda dos resultados: %.4f" % stats.mode(results))
print("Desvio padrão: %.4f" % stats.stdev(results))
