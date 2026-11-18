import sqlite3

from dao.professor_dao import ProfessorDAO
from utils.validacoes import inteiro_convertido, texto_valido, vazio

# Titulações aceitas pelo sistema (mesmos valores permitidos no banco)
TITULACOES = ("Doutor", "Mestre", "Especialista")


class Professor:
    """Representa um professor e concentra suas regras de negócio."""

    def __init__(self, dados):
        self._dados = dict(dados) if dados else {}
        self.errors = []

    def validate(self):
        """Valida os dados do professor e preenche a lista de erros."""
        self.errors = []

        matricula = self._dados.get("matricula")
        nome = self._dados.get("nome")
        titulacao = self._dados.get("titulacao")
        numero_departamento_bruto = self._dados.get("numero_departamento")

        numero_departamento = inteiro_convertido(numero_departamento_bruto)

        # Validação da matrícula
        if vazio(matricula):
            self.errors.append("A matrícula do professor é obrigatória.")

        # Validação do nome
        if vazio(nome):
            self.errors.append("O nome do professor é obrigatório.")

        elif not texto_valido(nome, 3):
            self.errors.append(
                "O nome deve possuir pelo menos 3 caracteres."
            )

        # Validação da titulação
        if titulacao not in TITULACOES:
            self.errors.append(
                "A titulação deve ser Doutor, Mestre ou Especialista."
            )

        # Validação do departamento
        if vazio(numero_departamento_bruto):
            self.errors.append("O departamento é obrigatório.")

        elif numero_departamento is None or numero_departamento <= 0:
            self.errors.append("O departamento selecionado é inválido.")

        if self.errors:
            return False

        self._dados.update({
            "matricula": str(matricula).strip(),
            "nome": str(nome).strip(),
            "titulacao": titulacao,
            "numero_departamento": numero_departamento
        })

        return True

    def save(self):
        """Valida e grava o professor no banco. Retorna True em caso de sucesso."""
        if not self.validate():
            return False

        try:
            ProfessorDAO.inserir(self._dados)

        except sqlite3.IntegrityError as erro:
            mensagem = str(erro)

            if "professor.matricula" in mensagem:
                self.errors.append(
                    "Já existe um professor com essa matrícula."
                )
            elif "FOREIGN KEY" in mensagem:
                self.errors.append(
                    "O departamento selecionado não existe."
                )
            else:
                self.errors.append(
                    "Não foi possível cadastrar o professor."
                )

            return False

        return True

    @staticmethod
    def exibir_professores():
        """Retorna todos os professores cadastrados."""
        return ProfessorDAO.listar()

    @staticmethod
    def verificar_matricula(matricula):
        """Busca um professor pela matrícula."""
        return ProfessorDAO.buscar_por_matricula(matricula)

    @staticmethod
    def atualizar_professor(matricula, dados):
        """Atualiza os dados de um professor existente."""
        return ProfessorDAO.atualizar(matricula, dados)

    @staticmethod
    def excluir_professor(matricula):
        """Remove o professor com a matrícula informada."""
        return ProfessorDAO.excluir(matricula)

    @property
    def matricula(self):
        return self._dados.get("matricula")

    @property
    def nome(self):
        return self._dados.get("nome")

    @property
    def titulacao(self):
        return self._dados.get("titulacao")

    @property
    def numero_departamento(self):
        return self._dados.get("numero_departamento")

    @property
    def departamento(self):
        return self._dados.get("departamento")
