from flask import Flask

import controllers.professor_controller


def registrar_rotas_professor(app: Flask):
    """Registra as rotas relacionadas a professores no aplicativo Flask."""
    app.add_url_rule(
        "/professores",
        endpoint="professores",
        view_func=controllers.professor_controller.listar_professores,
        methods=["GET"],
    )

    app.add_url_rule(
        "/professores/cadastrar",
        endpoint="cadastrar_professor",
        view_func=controllers.professor_controller.cadastrar_professor,
        methods=["GET", "POST"],
    )

    app.add_url_rule(
        "/professores/editar/<matricula>",
        endpoint="editar_professor",
        view_func=controllers.professor_controller.editar_professor,
        methods=["GET", "POST"],
    )

    app.add_url_rule(
        "/professores/remover/<matricula>",
        endpoint="remover_professor",
        view_func=controllers.professor_controller.remover_professor,
        methods=["POST"],
    )
