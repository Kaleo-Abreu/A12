from flask import Flask

from dao.conexao import criar_tabelas
from routers.departamento_router import registrar_rotas_departamento
from routers.professor_router import registrar_rotas_professor


app = Flask(__name__)

# Garante que as tabelas existam antes de iniciar o sistema
criar_tabelas()

# Registra as rotas de cada parte do sistema
registrar_rotas_departamento(app)
registrar_rotas_professor(app)

print("Banco de dados conectado e tabelas verificadas com sucesso!")

if __name__ == "__main__":
    app.run(debug=True)
