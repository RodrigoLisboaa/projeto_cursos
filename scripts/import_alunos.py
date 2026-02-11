import csv
from pathlib import Path
from core.alunos import normalizar_aluno, validar_aluno

def main():
    caminho_csv = Path("data") / "alunos.csv"
    validos = []
    invalidos = []

    with caminho_csv.open(mode="r", encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            linha = normalizar_aluno(linha)
            erros = validar_aluno(linha)

            if erros:
                invalidos.append((linha, erros))
            else:
                validos.append(linha)

    # Relatório no terminal
    for linha, erros in invalidos:
        aluno_id = linha.get("id")
        nome = (linha.get("nome") or "").strip()
        print(f"Aluno ID {aluno_id} ({nome}) inválido: {', '.join(erros)}")

    print(f"\n Total Válidos: {len(validos)}")
    print(f" Total inválidos: {len(invalidos)}")
    
    caminho_invalidos = Path("data") / "alunos_invalidos.csv"

    with caminho_invalidos.open(mode="w", encoding="utf-8", newline="") as f:
        campos = ["id", "nome", "email", "idade", "erros"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()

        for linha, erros in invalidos:
            writer.writerow({
                "id": linha.get("id"),
                "nome": linha.get("nome"),
                "email": linha.get("email"),
                "idade": linha.get("idade"),
                "erros": "; ".join(erros),
            })            

if __name__ == "__main__":
    main()