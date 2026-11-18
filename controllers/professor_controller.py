from flask import redirect, render_template, request, url_for

from models.departamento import Departamento
from models.professor import Professor


def listar_professores():
    """Lista todos os professores cadastrados."""
    professores = Professor.exibir_professores()

    return render_template(
        "professor/listar_professores.html",
        professores=professores
    )


def pagina_cadastro_professor():
    """Abre o formulário de cadastro de professor."""
    return render_template(
        "professor/cadastro.html",
        departamentos=Departamento.exibir_departamentos()
    )


def cadastrar_professor():
    """Cadastra um novo professor."""
    dados = {
        "matricula": request.form.get("matricula"),
        "nome": request.form.get("nome"),
        "titulacao": request.form.get("titulacao"),
        "numero_departamento": request.form.get("numero_departamento")
    }

    professor = Professor(dados)

    if professor.save():
        return render_template(
            "professor/resultado.html",
            erros=[],
            mensagem="Professor cadastrado com sucesso."
        )

    return render_template(
        "professor/resultado.html",
        erros=professor.errors
    )


def editar_professor(matricula):
    """Abre o formulário de edição do professor."""
    professor = Professor.verificar_matricula(matricula)

    if professor is None:
        return render_template(
            "erro.html",
            mensagem="Professor não encontrado."
        ), 404

    return render_template(
        "professor/editar_professor.html",
        professor=professor,
        departamentos=Departamento.exibir_departamentos(),
        erros=[]
    )


def salvar_edicao_professor(matricula):
    """Atualiza os dados do professor informado."""
    professor_atual = Professor.verificar_matricula(matricula)

    if professor_atual is None:
        return render_template(
            "erro.html",
            mensagem="Professor não encontrado."
        ), 404

    dados = {
        "matricula": matricula,
        "nome": request.form.get("nome"),
        "titulacao": request.form.get("titulacao"),
        "numero_departamento": request.form.get("numero_departamento")
    }

    professor = Professor(dados)

    if not professor.validate():
        return render_template(
            "professor/editar_professor.html",
            professor=professor_atual,
            departamentos=Departamento.exibir_departamentos(),
            erros=professor.errors
        ), 400

    Professor.atualizar_professor(matricula, professor._dados)

    return redirect(url_for("professores"))


def remover_professor(matricula):
    """Remove o professor com a matrícula informada."""
    professor = Professor.verificar_matricula(matricula)

    if professor is None:
        return render_template(
            "erro.html",
            mensagem="Professor não encontrado."
        ), 404

    Professor.excluir_professor(matricula)

    return redirect(url_for("professores"))
