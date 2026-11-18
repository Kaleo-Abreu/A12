from dao.conexao import conectar


class ProfessorDAO:

    @staticmethod
    def inserir(dados):
        """Insere um novo professor no banco de dados."""
        conexao = conectar()

        try:
            conexao.execute("""
                INSERT INTO professor (
                    matricula, nome, titulacao, numero_departamento
                )
                VALUES (?, ?, ?, ?)
            """, (
                dados["matricula"],
                dados["nome"],
                dados["titulacao"],
                dados["numero_departamento"]
            ))

            conexao.commit()
            return True

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    @staticmethod
    def listar():
        """Retorna todos os professores, incluindo a descrição do departamento."""
        conexao = conectar()

        try:
            return conexao.execute("""
                SELECT p.matricula, p.nome, p.titulacao,
                       p.numero_departamento, d.descricao AS departamento
                FROM professor p
                LEFT JOIN departamento d ON d.numero = p.numero_departamento
                ORDER BY p.nome
            """).fetchall()
        finally:
            conexao.close()

    @staticmethod
    def buscar_por_matricula(matricula):
        """Retorna um professor pela matrícula ou None caso não exista."""
        conexao = conectar()

        try:
            return conexao.execute("""
                SELECT p.matricula, p.nome, p.titulacao,
                       p.numero_departamento, d.descricao AS departamento
                FROM professor p
                LEFT JOIN departamento d ON d.numero = p.numero_departamento
                WHERE p.matricula = ?
            """, (matricula,)).fetchone()
        finally:
            conexao.close()

    @staticmethod
    def atualizar(matricula, dados):
        """Atualiza os dados do professor com a matrícula informada."""
        conexao = conectar()

        try:
            conexao.execute("""
                UPDATE professor
                SET nome = ?,
                    titulacao = ?,
                    numero_departamento = ?
                WHERE matricula = ?
            """, (
                dados["nome"],
                dados["titulacao"],
                dados["numero_departamento"],
                matricula
            ))

            conexao.commit()
            return True

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    @staticmethod
    def excluir(matricula):
        """Remove o professor com a matrícula informada."""
        conexao = conectar()

        try:
            conexao.execute(
                "DELETE FROM professor WHERE matricula = ?",
                (matricula,)
            )

            conexao.commit()
            return True

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()
