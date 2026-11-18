from dao.conexao import conectar


class DepartamentoDAO:

    @staticmethod
    def inserir(dados):
        """Insere um novo departamento no banco de dados."""
        conexao = conectar()

        try:
            conexao.execute("""
                INSERT INTO departamento (numero, descricao)
                VALUES (?, ?)
            """, (
                dados["numero"],
                dados["descricao"]
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
        """Retorna todos os departamentos cadastrados."""
        conexao = conectar()

        try:
            return conexao.execute(
                "SELECT * FROM departamento ORDER BY numero"
            ).fetchall()
        finally:
            conexao.close()

    @staticmethod
    def buscar_por_numero(numero):
        """Retorna um departamento pelo número ou None caso não exista."""
        conexao = conectar()

        try:
            return conexao.execute(
                "SELECT * FROM departamento WHERE numero = ?",
                (numero,)
            ).fetchone()
        finally:
            conexao.close()

    @staticmethod
    def atualizar(numero, dados):
        """Atualiza a descrição do departamento com o número informado."""
        conexao = conectar()

        try:
            conexao.execute("""
                UPDATE departamento
                SET descricao = ?
                WHERE numero = ?
            """, (
                dados["descricao"],
                numero
            ))

            conexao.commit()
            return True

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    @staticmethod
    def excluir(numero):
        """Remove o departamento com o número informado."""
        conexao = conectar()

        try:
            conexao.execute(
                "DELETE FROM departamento WHERE numero = ?",
                (numero,)
            )

            conexao.commit()
            return True

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()
