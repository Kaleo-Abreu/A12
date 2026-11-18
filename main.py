from flask import Flask

from dao.conexao import criar_tabelas
from routers.departamento_router import iniciar_rotas_departamento
from routers.professor_router import iniciar_rotas_professor


app = Flask(__name__)

# Garante que as tabelas existam antes de iniciar o sistema
criar_tabelas()

# Registra as rotas de cada parte do sistema
iniciar_rotas_departamento(app)
iniciar_rotas_professor(app)


if __name__ == "__main__":
    app.run(debug=True)
