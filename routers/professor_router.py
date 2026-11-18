from flask import Flask

import controllers.professor_controller


def iniciar_rotas_professor(app: Flask):
    """Registra as rotas relacionadas a professores no aplicativo Flask."""
    app.add_url_rule(
        "/professores",
        endpoint="professores",
        view_func=controllers.professor_controller.listar_professores,
        methods=["GET"]
    )

    app.add_url_rule(
        "/professores/cadastrar",
        endpoint="pagina_cadastro_professor",
        view_func=controllers.professor_controller.pagina_cadastro_professor,
        methods=["GET"]
    )

    app.add_url_rule(
        "/professores/cadastrar",
        endpoint="cadastrar_professor",
        view_func=controllers.professor_controller.cadastrar_professor,
        methods=["POST"]
    )

    app.add_url_rule(
        "/professores/editar/<matricula>",
        endpoint="editar_professor",
        view_func=controllers.professor_controller.editar_professor,
        methods=["GET"]
    )

    app.add_url_rule(
        "/professores/editar/<matricula>",
        endpoint="salvar_edicao_professor",
        view_func=controllers.professor_controller.salvar_edicao_professor,
        methods=["POST"]
    )

    app.add_url_rule(
        "/professores/remover/<matricula>",
        endpoint="remover_professor",
        view_func=controllers.professor_controller.remover_professor,
        methods=["POST"]
    )
