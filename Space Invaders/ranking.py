import os

def mostrar_ranking():
    if not os.path.exists("ranking.txt"):
        print("Nenhum ranking disponível.")
        return

    ranking = []
    with open("ranking.txt", "r") as f:
        linhas = f.readlines()
        for linha in linhas:
            nome, pontuacao, data = linha.strip().split(",")
            ranking.append((nome, int(pontuacao), data))

    ranking.sort(key=lambda x: x[1], reverse=True)  # Ordena pelo campo pontuação

    print("Ranking:")
    for i, (nome, pontuacao, data) in enumerate(ranking[:5]):
        print(f"{i+1}. {nome} - {pontuacao} pontos em {data}")
