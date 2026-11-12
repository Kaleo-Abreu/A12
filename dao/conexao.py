import sqlite3
from contextlib import contextmanager


def conectar():
    """Abre e retorna uma conexão com o banco de dados SQLite."""
    conexao = sqlite3.connect("sistema.db")

    # Permite acessar as colunas pelo nome (ex.: linha["descricao"])
    conexao.row_factory = sqlite3.Row

    # Ativa a verificação de chaves estrangeiras no SQLite
    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao


@contextmanager
def conexao_banco():
    """Abre uma conexão, confirma as alterações e fecha ao final (mesmo com erro)."""
    conexao = conectar()

    try:
        yield conexao
        conexao.commit()  # Confirma (salva) as alterações
    except Exception:
        conexao.rollback()  # Desfaz a operação em caso de erro
        raise
    finally:
        conexao.close()  # Garante que a conexão seja sempre fechada


def criar_tabelas():
    """Cria as tabelas 'departamento' e 'professor' caso ainda não existam."""
    with conexao_banco() as conexao:
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS departamento (
                numero INTEGER PRIMARY KEY,
                descricao TEXT NOT NULL
            )
        """)

        cursor.execute("""
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
