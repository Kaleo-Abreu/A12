from flask import abort, render_template, request

from models.departamento import Departamento


def exibir_inicio():
    """Exibe a página inicial do sistema."""
    return render_template("index.html")


def cadastrar_departamento():
    """Abre o formulário (GET) ou cadastra um novo departamento (POST)."""
    if request.method == "GET":
        return render_template("departamento/cadastro.html")

    dados = {
        "numero": request.form.get("numero"),
        "descricao": request.form.get("descricao"),
    }

    departamento = Departamento(dados)

    if departamento.inserir():
        return render_template(
            "departamento/resultado.html",
            erros=[],
            mensagem="Departamento cadastrado com sucesso.",
        )

    return render_template(
        "departamento/resultado.html",
        erros=departamento.erros,
    )


def listar_departamentos():
    """Lista todos os departamentos cadastrados."""
    departamentos = Departamento.listar_todos()

    return render_template(
        "departamento/listar_departamentos.html",
        departamentos=departamentos,
    )


def editar_departamento(id):
    """Abre o formulário (GET) ou atualiza a descrição do departamento (POST)."""
    departamento = Departamento.buscar_por_numero(id)
    if departamento is None:
        abort(404)

    if request.method == "GET":
        return render_template(
            "departamento/editar_departamento.html",
            departamento=departamento,
            erros=[],
        )

    dados = {
        "numero": id,
        "descricao": request.form.get("descricao"),
    }
    departamento_editado = Departamento(dados)

    if not departamento_editado.validar():
        return render_template(
            "departamento/editar_departamento.html",
            departamento=departamento,
            erros=departamento_editado.erros,
        )

    Departamento.atualizar(id, dados["descricao"].strip())
    return render_template(
        "departamento/resultado.html",
        erros=[],
        mensagem="Departamento atualizado com sucesso.",
    )


def remover_departamento(id):
    """Remove o departamento com o número informado."""
    departamento = Departamento.buscar_por_numero(id)
    if departamento is None:
        abort(404)

    Departamento.remover(id)
    return render_template(
        "departamento/resultado.html",
        erros=[],
        mensagem="Departamento removido com sucesso.",
    )
