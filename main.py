import pandas as pd
import pydot

tabela = pd.read_csv("Baseparateste.csv", delimiter=";")

# Lista de todas as pastas para poder gerar os nós.
# utilizamos um set() porque não queremos pastas duplicadas.
todas_pastas = set()

# Um mapa de conexões onde a chava é a pasta de origem, que mapeia
# para um set de tuplas onde o primeiro elemento da tupla é a pasta destino ou backup
# e o segundo elemento é o nome da aplicação.
todas_conexoes = {}

def normalizar_pasta(f):
    if pd.isnull(f):
        return ""
    return f.replace("\\", "_").replace(":", "")

for _, row in tabela.iterrows():
    nome = row["Nome"]
    origem = normalizar_pasta(row["PastaOrigem"])
    destino = normalizar_pasta(row["PastaDestino"])
    backup = normalizar_pasta(row["PastaBackup"])

    for p in [origem, destino, backup]:
        if p.strip() == "":
            continue
        todas_pastas.add(p)

    # PASTA ORIGEM -> [
    #     (backup/destino, A)
    #     (backup/destino, B)
    #     (backup/destino, C)
    #     (backup/destino, D)
    # ]
    for p in [destino, backup]:
        if p.strip() == "":
            continue
        if origem not in todas_conexoes:
            todas_conexoes[origem] = []

        todas_conexoes[origem].append((p, nome))

# https://github.com/pydot/pydot
grafico = pydot.Dot(graph_type='digraph', bgcolor="white")

# Add nodes
for pasta in todas_pastas:
    node = pydot.Node(pasta, label=pasta)
    grafico.add_node(node)

# Add edges
for orig, conex in todas_conexoes.items():
    for c in conex:
        grafico.add_edge(pydot.Edge(orig, c[0], color="blue", label=c[1]))

grafico.write_png("resultado.png")
