from flask import abort, render_template, request

from models.departamento import Departamento
from models.professor import Professor


def listar_professores():
    """Lista todos os professores cadastrados."""
    professores = Professor.listar_todos()

    return render_template(
        "professor/listar_professores.html",
        professores=professores,
    )


def cadastrar_professor():
    """Abre o formulário (GET) ou cadastra um novo professor (POST)."""
    if request.method == "GET":
        return render_template(
            "professor/cadastro.html",
            departamentos=Departamento.listar_todos(),
        )

    dados = {
        "matricula": request.form.get("matricula"),
        "nome": request.form.get("nome"),
        "titulacao": request.form.get("titulacao"),
        "numero_departamento": request.form.get("numero_departamento"),
    }

    professor = Professor(dados)

    if professor.inserir():
        return render_template(
            "professor/resultado.html",
            erros=[],
            mensagem="Professor cadastrado com sucesso.",
        )

    return render_template(
        "professor/resultado.html",
        erros=professor.erros,
    )


def editar_professor(matricula):
    """Abre o formulário (GET) ou atualiza os dados do professor (POST)."""
    professor = Professor.buscar_por_matricula(matricula)
    if professor is None:
        abort(404)

    departamentos = Departamento.listar_todos()

    if request.method == "GET":
        return render_template(
            "professor/editar_professor.html",
            professor=professor,
            departamentos=departamentos,
            erros=[],
        )

    dados = {
        "matricula": matricula,
        "nome": request.form.get("nome"),
        "titulacao": request.form.get("titulacao"),
        "numero_departamento": request.form.get("numero_departamento"),
    }
    professor_editado = Professor(dados)

    if not professor_editado.validar():
        return render_template(
            "professor/editar_professor.html",
            professor=professor,
            departamentos=departamentos,
            erros=professor_editado.erros,
        )

    Professor.atualizar(
        matricula,
        dados["nome"].strip(),
        dados["titulacao"],
        int(dados["numero_departamento"]),
    )

    return render_template(
        "professor/resultado.html",
        erros=[],
        mensagem="Professor atualizado com sucesso.",
    )


def remover_professor(matricula):
    """Remove o professor com a matrícula informada."""
    professor = Professor.buscar_por_matricula(matricula)
    if professor is None:
        abort(404)

    Professor.remover(matricula)

    return render_template(
        "professor/resultado.html",
        erros=[],
        mensagem="Professor removido com sucesso.",
    )
