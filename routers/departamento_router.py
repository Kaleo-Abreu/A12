from flask import Flask

import controllers.departamento_controller


def registrar_rotas_departamento(app: Flask):
    """Registra as rotas relacionadas a departamentos no aplicativo Flask."""
    app.add_url_rule(
        "/",
        endpoint="inicio",
        view_func=controllers.departamento_controller.exibir_inicio,
        methods=["GET"],
    )

    app.add_url_rule(
        "/departamentos/cadastrar",
        endpoint="cadastrar_departamento",
        view_func=controllers.departamento_controller.cadastrar_departamento,
        methods=["GET", "POST"],
    )

    app.add_url_rule(
        "/departamentos",
        endpoint="departamentos",
        view_func=controllers.departamento_controller.listar_departamentos,
        methods=["GET"],
    )

    app.add_url_rule(
        "/departamentos/editar/<int:id>",
        endpoint="editar_departamento",
        view_func=controllers.departamento_controller.editar_departamento,
        methods=["GET", "POST"],
    )

    app.add_url_rule(
        "/departamentos/remover/<int:id>",
        endpoint="remover_departamento",
        view_func=controllers.departamento_controller.remover_departamento,
        methods=["POST"],
    )
