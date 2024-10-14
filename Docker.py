from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/lista_presenca'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Presença para alunos
class Presenca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_aluno = db.Column(db.String(100), nullable=False)
    data_presenca = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(10), nullable=False)  # 'Presente' ou 'Ausente'

# Criação do banco de dados
with app.app_context():
    db.create_all()

# Rotas CRUD
# Registrar presença de um aluno
@app.route('/presencas', methods=['POST'])
def registrar_presenca():
    data = request.get_json()
    nova_presenca = Presenca(
        nome_aluno=data['nome_aluno'], 
        status=data['status']  # 'Presente' ou 'Ausente'
    )
    db.session.add(nova_presenca)
    db.session.commit()
    return jsonify({'id': nova_presenca.id}), 201

# Listar todas as presenças
@app.route('/presencas', methods=['GET'])
def listar_presencas():
    presencas = Presenca.query.all()
    presencas_list = [
        {'id': p.id, 'nome_aluno': p.nome_aluno, 'status': p.status, 
         'data_presenca': p.data_presenca.strftime('%Y-%m-%d')} 
        for p in presencas
    ]
    return jsonify(presencas_list), 200

# Obter presença por ID
@app.route('/presencas/<int:id>', methods=['GET'])
def obter_presenca(id):
    presenca = Presenca.query.get_or_404(id)
    return jsonify({
        'id': presenca.id, 
        'nome_aluno': presenca.nome_aluno, 
        'status': presenca.status,
        'data_presenca': presenca.data_presenca.strftime('%Y-%m-%d')
    }), 200

# Atualizar presença de um aluno
@app.route('/presencas/<int:id>', methods=['PUT'])
def atualizar_presenca(id):
    data = request.get_json()
    presenca = Presenca.query.get_or_404(id)
    presenca.nome_aluno = data['nome_aluno']
    presenca.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Presença atualizada com sucesso'}), 200

# Deletar registro de presença
@app.route('/presencas/<int:id>', methods=['DELETE'])
def deletar_presenca(id):
    presenca = Presenca.query.get_or_404(id)
    db.session.delete(presenca)
    db.session.commit()
    return jsonify({'message': 'Registro de presença deletado com sucesso'}), 200

# Rota para renderizar o front-end
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
