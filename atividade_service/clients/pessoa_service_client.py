import requests

PESSOA_SERVICE_URL = "http://localhost:8086/pessoas"

class PessoaServiceClient:
    @staticmethod
    def verificar_leciona(id_professor, id_disciplina):
        url = f"{PESSOA_SERVICE_URL}/leciona/{id_professor}/{id_disciplina}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get('leciona', False) if data.get('isok') else False
        except requests.RequestException as e:
            print(f"Erro ao acessar o pessoa_service: {e}")
            return False
        

    @staticmethod
    def listar_professores():
        url = f"{PESSOA_SERVICE_URL}/professores"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()            
        except requests.RequestException as e:
            print(f"Erro ao acessar o pessoa_service: {e}")
            return False
        
    @staticmethod
    def listar_alunos():
        url = f"{PESSOA_SERVICE_URL}/alunos"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()            
        except requests.RequestException as e:
            print(f"Erro ao acessar o pessoa_service: {e}")
            return False

    @staticmethod
    def listar_disciplinas():
        url = f"{PESSOA_SERVICE_URL}/disciplinas"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()            
        except requests.RequestException as e:
            print(f"Erro ao acessar o pessoa_service: {e}")
            return False