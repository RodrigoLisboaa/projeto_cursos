import csv
from pathlib import Path

def normalizar_aluno(linha:dict) -> dict:
    return {
        "id": (linha.get("id") or "").strip(),
        "nome": " ".join(((linha.get("nome") or "").strip()).split()),
        "email": ((linha.get("email") or "").strip()).lower(),
        "idade": (linha.get("idade") or "").strip(),
    }

def validar_aluno(linha: dict) -> list[str]:
    erros = []

    # 1)email obrigatório
    email = (linha.get("email") or "").strip()
    if not email:
        erros.append("email vazio")

    # 2) idade obrigatória, numérica e >=16
    idade_texto = (linha.get("idade") or "").strip()
    if not idade_texto:
        erros.append("idade vazia")
    else:
        try:
            idade = int(idade_texto)
            if idade < 16:
                erros.append("idade menor que 16")
        except ValueError:
            erros.append("idade não é um número")

    return erros

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