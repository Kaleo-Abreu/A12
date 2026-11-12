import sqlite3

from dao import departamento_dao


class Departamento:
    """Representa um departamento e concentra suas regras de negócio."""

    def __init__(self, dados):
        self._dados = dict(dados) if dados else {}
        self.erros = []

    def validar(self):
        """Valida os dados do departamento e preenche a lista de erros."""
        self.erros = []

        numero = self._dados.get("numero")
        descricao = self._dados.get("descricao")

        # Validação do número
        if numero is None or str(numero).strip() == "":
            self.erros.append("O número do departamento é obrigatório.")
        else:
            try:
                numero = int(numero)

                if numero <= 0:
                    self.erros.append("O número do departamento deve ser positivo.")

            except (ValueError, TypeError):
                self.erros.append("O número do departamento deve ser um número inteiro.")

        # Validação da descrição
        if descricao is None or str(descricao).strip() == "":
            self.erros.append("A descrição do departamento é obrigatória.")

        elif len(str(descricao).strip()) < 3:
            self.erros.append("A descrição deve possuir pelo menos 3 caracteres.")

        return len(self.erros) == 0

    def inserir(self):
        """Valida e grava o departamento no banco. Retorna True em caso de sucesso."""
        if not self.validar():
            return False

        try:
            departamento_dao.inserir(
                int(self._dados.get("numero")),
                str(self._dados.get("descricao")).strip(),
            )
        except sqlite3.IntegrityError:
            # Acontece, por exemplo, quando o número (chave primária) já existe
            self.erros.append("Já existe um departamento com esse número.")
            return False

        return True

    @staticmethod
    def buscar_por_numero(numero):
        """Busca um departamento pelo número."""
        return departamento_dao.buscar_por_numero(numero)

    @staticmethod
    def listar_todos():
        """Retorna todos os departamentos cadastrados."""
        return departamento_dao.listar_todos()

    @staticmethod
    def atualizar(numero, descricao):
        """Atualiza a descrição de um departamento existente."""
        departamento_dao.atualizar(numero, descricao)

    @staticmethod
    def remover(numero):
        """Remove o departamento com o número informado."""
        departamento_dao.remover(numero)
