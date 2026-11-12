from dao.conexao import conexao_banco


def inserir(matricula, nome, titulacao, numero_departamento):
    """Insere um novo professor no banco de dados."""
    with conexao_banco() as conexao:
        conexao.execute("""
            INSERT INTO professor (matricula, nome, titulacao, numero_departamento)
            VALUES (?, ?, ?, ?)
        """, (matricula, nome, titulacao, numero_departamento))


def listar_todos():
    """Retorna todos os professores, incluindo a descrição do departamento."""
    with conexao_banco() as conexao:
        cursor = conexao.execute("""
            SELECT p.matricula, p.nome, p.titulacao,
                   p.numero_departamento, d.descricao AS departamento
            FROM professor p
            LEFT JOIN departamento d ON d.numero = p.numero_departamento
            ORDER BY p.nome
        """)

        return cursor.fetchall()  # Retorna todas as linhas encontradas


def buscar_por_matricula(matricula):
    """Retorna um professor pela matrícula ou None caso não exista."""
    with conexao_banco() as conexao:
        cursor = conexao.execute("""
            SELECT p.matricula, p.nome, p.titulacao,
                   p.numero_departamento, d.descricao AS departamento
            FROM professor p
            LEFT JOIN departamento d ON d.numero = p.numero_departamento
            WHERE p.matricula = ?
        """, (matricula,))

        return cursor.fetchone()  # Retorna apenas uma linha (ou None)


def atualizar(matricula, nome, titulacao, numero_departamento):
    """Atualiza os dados do professor com a matrícula informada."""
    with conexao_banco() as conexao:
        conexao.execute("""
            UPDATE professor
            SET nome = ?, titulacao = ?, numero_departamento = ?
            WHERE matricula = ?
        """, (nome, titulacao, numero_departamento, matricula))


def remover(matricula):
    """Remove o professor com a matrícula informada."""
    with conexao_banco() as conexao:
        conexao.execute("""
            DELETE FROM professor
            WHERE matricula = ?
        """, (matricula,))
