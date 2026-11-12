from dao.conexao import conexao_banco


def inserir(numero, descricao):
    """Insere um novo departamento no banco de dados."""
    with conexao_banco() as conexao:
        conexao.execute("""
            INSERT INTO departamento (numero, descricao)
            VALUES (?, ?)
        """, (numero, descricao))


def listar_todos():
    """Retorna todos os departamentos cadastrados."""
    with conexao_banco() as conexao:
        cursor = conexao.execute("""
            SELECT * FROM departamento
        """)

        return cursor.fetchall()  # Retorna todas as linhas encontradas


def atualizar(numero, descricao):
    """Atualiza a descrição do departamento com o número informado."""
    with conexao_banco() as conexao:
        conexao.execute("""
            UPDATE departamento
            SET descricao = ?
            WHERE numero = ?
        """, (descricao, numero))


def remover(numero):
    """Remove o departamento com o número informado."""
    with conexao_banco() as conexao:
        conexao.execute("""
            DELETE FROM departamento
            WHERE numero = ?
        """, (numero,))


def buscar_por_numero(numero):
    """Retorna um departamento pelo número ou None caso não exista."""
    with conexao_banco() as conexao:
        cursor = conexao.execute("""
            SELECT * FROM departamento
            WHERE numero = ?
        """, (numero,))

        return cursor.fetchone()  # Retorna apenas uma linha (ou None)
