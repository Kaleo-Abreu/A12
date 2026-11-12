import sqlite3

from dao import professor_dao

# Titulações aceitas pelo sistema (mesmos valores permitidos no banco)
TITULACOES = ("Doutor", "Mestre", "Especialista")


class Professor:
    """Representa um professor e concentra suas regras de negócio."""

    def __init__(self, dados):
        self._dados = dict(dados) if dados else {}
        self.erros = []

    def validar(self):
        """Valida os dados do professor e preenche a lista de erros."""
        self.erros = []

        matricula = self._dados.get("matricula")
        nome = self._dados.get("nome")
        titulacao = self._dados.get("titulacao")
        numero_departamento = self._dados.get("numero_departamento")

        # Validação da matrícula
        if matricula is None or str(matricula).strip() == "":
            self.erros.append("A matrícula do professor é obrigatória.")

        # Validação do nome
        if nome is None or str(nome).strip() == "":
            self.erros.append("O nome do professor é obrigatório.")

        elif len(str(nome).strip()) < 3:
            self.erros.append("O nome deve possuir pelo menos 3 caracteres.")

        # Validação da titulação
        if titulacao not in TITULACOES:
            self.erros.append("A titulação deve ser Doutor, Mestre ou Especialista.")

        # Validação do departamento
        if numero_departamento is None or str(numero_departamento).strip() == "":
            self.erros.append("O departamento é obrigatório.")
        else:
            try:
                if int(numero_departamento) <= 0:
                    self.erros.append("O departamento selecionado é inválido.")

            except (ValueError, TypeError):
                self.erros.append("O departamento selecionado é inválido.")

        return len(self.erros) == 0

    def inserir(self):
        """Valida e grava o professor no banco. Retorna True em caso de sucesso."""
        if not self.validar():
            return False

        try:
            professor_dao.inserir(
                str(self._dados.get("matricula")).strip(),
                str(self._dados.get("nome")).strip(),
                self._dados.get("titulacao"),
                int(self._dados.get("numero_departamento")),
            )
        except sqlite3.IntegrityError as erro:
            mensagem = str(erro)

            if "professor.matricula" in mensagem:
                self.erros.append("Já existe um professor com essa matrícula.")
            elif "FOREIGN KEY" in mensagem:
                self.erros.append("O departamento selecionado não existe.")
            else:
                self.erros.append("Não foi possível cadastrar o professor.")

            return False

        return True

    @staticmethod
    def buscar_por_matricula(matricula):
        """Busca um professor pela matrícula."""
        return professor_dao.buscar_por_matricula(matricula)

    @staticmethod
    def listar_todos():
        """Retorna todos os professores cadastrados."""
        return professor_dao.listar_todos()

    @staticmethod
    def atualizar(matricula, nome, titulacao, numero_departamento):
        """Atualiza os dados de um professor existente."""
        professor_dao.atualizar(matricula, nome, titulacao, numero_departamento)

    @staticmethod
    def remover(matricula):
        """Remove o professor com a matrícula informada."""
        professor_dao.remover(matricula)
