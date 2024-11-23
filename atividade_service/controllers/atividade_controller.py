from flask import Blueprint, jsonify, request
from models import atividade_model
from clients.pessoa_service_client import PessoaServiceClient

atividade_bp = Blueprint('atividade_bp', __name__)

@atividade_bp.route('/', methods=['GET'])
def listar_atividades():
    atividades = atividade_model.listar_atividades()
    return jsonify(atividades)

@atividade_bp.route('/<int:id_atividade>', methods=['GET'])
def obter_atividade(id_atividade):
    try:
        atividade = atividade_model.obter_atividade(id_atividade)
        return jsonify(atividade)
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404

@atividade_bp.route('/<int:id_atividade>/professor/<int:id_professor>', methods=['GET'])
def obter_atividade_para_professor(id_atividade, id_professor):
    try:
        atividade = atividade_model.obter_atividade(id_atividade)
        if not PessoaServiceClient.verificar_leciona(id_professor, atividade['id_disciplina']):
            atividade = atividade.copy()
            atividade.pop('respostas', None)
        return jsonify(atividade)
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404



@atividade_bp.route('/salvar_atividade', methods=['POST'])
def salvar_atividade():
    try:
        atividade = request.json
        
        retorno = validacao(atividade, True)

        if (retorno > 0):
            atividade_model.salvar_atividade(atividade)
            return jsonify('Atividade salva com sucesso'), 200
        else:
            if retorno == -1:
                return jsonify({'erro': 'Formato incorreto'}), 404
            if retorno == -2:
                return jsonify({'erro': 'Preenchimento incorreto'}), 404
            if retorno == -3:
                return jsonify({'erro': 'id da disciplina/aluno inválido'}), 404 

    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404
    
@atividade_bp.route('/alterar_atividade', methods=['POST', 'PUT'])
def alterar_atividade():
    try:
        atividade = request.json
        
        retorno = validacao(atividade, False)

        if (retorno > 0):
            atividade_model.alterar_atividade(atividade)
            return jsonify('Atividade alterada com sucesso'), 200
        else:
            if retorno == -1:
                return jsonify({'erro': 'Formato incorreto'}), 404
            if retorno == -2:
                return jsonify({'erro': 'Preenchimento incorreto'}), 404
            if retorno == -3:
                return jsonify({'erro': 'id da disciplina/aluno inválido'}), 404 

    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404
    
@atividade_bp.route('/excluir_atividade', methods=["DELETE","POST"])
def excluir_atividade():
    try:
        atividade = request.json
        atividade_model.excluir_atividade(atividade['id_atividade'])
        return jsonify('Atividade excluída com sucesso'), 200
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404
    
def validacao(atividade, novo_registro):
        
        if ("id_atividade" not in atividade or "enunciado" not in atividade or 
            "id_disciplina" not in atividade or "respostas" not in atividade):
            return -1
            #return jsonify({'erro': 'Formato incorreto'}), 404
 
        if ((atividade["id_atividade"] > 0 and novo_registro == True) or 
            atividade["id_atividade"] == 0 and novo_registro == False):
            return -2
            #return jsonify({'erro': 'Preenchimento incorreto'}), 404

        if (atividade["enunciado"] == None or 
            atividade["id_disciplina"] == None or atividade["respostas"] == None):
            return -2
            #return jsonify({'erro': 'Preenchimento incorreto'}), 404

        disciplinas = PessoaServiceClient.listar_disciplinas()
        disciplina_valida = False
        for disciplina in disciplinas:
            if (disciplina["id_disciplina"] == atividade["id_disciplina"]):
                disciplina_valida = True
                break        
        
        if (disciplina_valida == False):
            return -3
            #return jsonify({'erro': 'id da disciplina/aluno inválido'}), 404    

        alunos = PessoaServiceClient.listar_alunos()
        if (len(atividade["respostas"]) > 0):
            for resposta in atividade["respostas"]:
                if ( "id_aluno" not in resposta or "nota" not in resposta or "resposta" not in resposta):
                    return -1
                    #return jsonify({'erro': 'Formato incorreto'}), 404
                
                aluno_valido = False 
                for aluno in alunos:                        
                    if (aluno["id_aluno"] == resposta["id_aluno"]):
                        aluno_valido = True
                        break
                    
                if (aluno_valido == False):
                    return -3
                    #return jsonify({'erro': 'id do aluno/aluno inválido'}), 404        
        return 1

    