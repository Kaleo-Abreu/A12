import sqlite3

from dao.departamento_dao import DepartamentoDAO
from utils.validacoes import inteiro_convertido, texto_valido, vazio


class Departamento:
    """Representa um departamento e concentra suas regras de negócio."""

    def __init__(self, dados):
        self._dados = dict(dados) if dados else {}
        self.errors = []

    def validate(self):
        """Valida os dados do departamento e preenche a lista de erros."""
        self.errors = []

        numero_bruto = self._dados.get("numero")
        descricao = self._dados.get("descricao")

        numero = inteiro_convertido(numero_bruto)

        # Validação do número
        if vazio(numero_bruto):
            self.errors.append(
                "O número do departamento é obrigatório."
            )

        elif numero is None:
            self.errors.append(
                "O número do departamento deve ser um número inteiro."
            )

        elif numero <= 0:
            self.errors.append(
                "O número do departamento deve ser positivo."
            )

        # Validação da descrição
        if vazio(descricao):
            self.errors.append(
                "A descrição do departamento é obrigatória."
            )

        elif not texto_valido(descricao, 3):
            self.errors.append(
                "A descrição deve possuir pelo menos 3 caracteres."
            )

        if self.errors:
            return False

        self._dados.update({
            "numero": numero,
            "descricao": str(descricao).strip()
        })

        return True

    def save(self):
        """Valida e grava o departamento no banco. Retorna True em caso de sucesso."""
        if not self.validate():
            return False

        try:
            DepartamentoDAO.inserir(self._dados)

        except sqlite3.IntegrityError:
            # Acontece, por exemplo, quando o número (chave primária) já existe
            self.errors.append(
                "Já existe um departamento com esse número."
            )
            return False

        return True

    @staticmethod
    def exibir_departamentos():
        """Retorna todos os departamentos cadastrados."""
        return DepartamentoDAO.listar()

    @staticmethod
    def verificar_numero(numero):
        """Busca um departamento pelo número."""
        return DepartamentoDAO.buscar_por_numero(numero)

    @staticmethod
    def atualizar_departamento(numero, dados):
        """Atualiza a descrição de um departamento existente."""
        return DepartamentoDAO.atualizar(numero, dados)

    @staticmethod
    def excluir_departamento(numero):
        """Remove o departamento com o número informado."""
        return DepartamentoDAO.excluir(numero)

    @property
    def numero(self):
        return self._dados.get("numero")

    @property
    def descricao(self):
        return self._dados.get("descricao")
