import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).resolve().parent.parent / "sistema.db"


def conectar():
    """Abre e retorna uma conexão com o banco de dados SQLite."""
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row

    # Ativa a verificação de chaves estrangeiras no SQLite
    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao


def criar_tabelas():
    """Cria as tabelas 'departamento' e 'professor' caso ainda não existam."""
    conexao = conectar()

    try:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS departamento (
                numero INTEGER PRIMARY KEY,
                descricao TEXT NOT NULL
            )
        """)

        conexao.execute("""
            CREATE TABLE IF NOT EXISTS professor (
                matricula TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                titulacao TEXT NOT NULL,

                numero_departamento INTEGER NOT NULL,

                CHECK (
                    titulacao IN (
                        'Doutor',
                        'Mestre',
                        'Especialista'
                    )
                ),

                FOREIGN KEY (numero_departamento)
                REFERENCES departamento(numero)
            )
        """)

        conexao.commit()

    finally:
        conexao.close()
