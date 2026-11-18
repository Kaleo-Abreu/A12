import sqlite3

from flask import redirect, render_template, request, url_for

from models.departamento import Departamento


def inicio():
    """Exibe a página inicial do sistema."""
    return render_template("index.html")


def pagina_cadastro_departamento():
    """Abre o formulário de cadastro de departamento."""
    return render_template("departamento/cadastro.html")


def cadastrar_departamento():
    """Cadastra um novo departamento."""
    dados = {
        "numero": request.form.get("numero"),
        "descricao": request.form.get("descricao")
    }

    departamento = Departamento(dados)

    if departamento.save():
        return render_template(
            "departamento/resultado.html",
            erros=[],
            mensagem="Departamento cadastrado com sucesso."
        )

    return render_template(
        "departamento/resultado.html",
        erros=departamento.errors
    )


def listar_departamentos():
    """Lista todos os departamentos cadastrados."""
    departamentos = Departamento.exibir_departamentos()

    return render_template(
        "departamento/listar_departamentos.html",
        departamentos=departamentos
    )


def editar_departamento(id):
    """Abre o formulário de edição do departamento."""
    departamento = Departamento.verificar_numero(id)

    if departamento is None:
        return render_template(
            "erro.html",
            mensagem="Departamento não encontrado."
        ), 404

    return render_template(
        "departamento/editar_departamento.html",
        departamento=departamento,
        erros=[]
    )


def salvar_edicao_departamento(id):
    """Atualiza a descrição do departamento informado."""
    departamento_atual = Departamento.verificar_numero(id)

    if departamento_atual is None:
        return render_template(
            "erro.html",
            mensagem="Departamento não encontrado."
        ), 404

    dados = {
        "numero": id,
        "descricao": request.form.get("descricao")
    }

    departamento = Departamento(dados)

    if not departamento.validate():
        return render_template(
            "departamento/editar_departamento.html",
            departamento=departamento_atual,
            erros=departamento.errors
        ), 400

    Departamento.atualizar_departamento(id, departamento._dados)

    return redirect(url_for("departamentos"))


def remover_departamento(id):
    """Remove o departamento com o número informado."""
    departamento = Departamento.verificar_numero(id)

    if departamento is None:
        return render_template(
            "erro.html",
            mensagem="Departamento não encontrado."
        ), 404

    try:
        Departamento.excluir_departamento(id)

    except sqlite3.IntegrityError:
        return render_template(
            "departamento/resultado.html",
            erros=[
                "Não é possível remover um departamento "
                "que possui professores cadastrados."
            ]
        )

    return redirect(url_for("departamentos"))
