from fastapi import FastAPI, Body, Depends, HTTPException   
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

app = FastAPI()

class Livro(BaseModel):
    titulo: str
    autor: str
    ano: int

class Autor(BaseModel):
    nome: str
    idade: int

class Usuario(BaseModel):
    nome: str
    email: str


dicionario_livros = {}

@app.get("/")
def read_root():
    return {"message": "OK"}

@app.get("/livros/")
def listar_livros(pagina: int = 1, tamanho: int = 3):
    pagina_inicial = (pagina - 1) * tamanho
    pagina_final = pagina_inicial + tamanho
  
    #convertendo o dicionário de livros em uma lista de tuplas (id, livro)
    lista_livro = list(dicionario_livros.items())

    #cortando a nossa lista de livros para retornar apenas os livros da página solicitada
    lista_livro_page = lista_livro[pagina_inicial:pagina_final]

    livros_pag= []

    for id, livro in lista_livro_page:
        livro_dict = {
            "id": id,
            "titulo": livro.titulo,
            "autor": livro.autor,
            "ano": livro.ano
        }

        livros_pag.append(livro_dict)

    return {
        "page=": pagina,
        "size=": tamanho,
        "livros": livros_pag
        }

def pega_ano(dicionario_livros):
       return  dicionario_livros['ano']

@app.get("/livros/ordenados-ano")
def listar_livros_ordenados():
    lista_livros = []
    for id, livro in dicionario_livros.items():
        
        livro_dict = {
            "id": id,
            "titulo": livro.titulo,
            "autor": livro.autor,
            "ano": livro.ano
        }

        lista_livros.append(livro_dict)

    lista_livros_ordenada = sorted(lista_livros, key=pega_ano)

    return {"livros_ordenados_ano": lista_livros_ordenada}




@app.post("/livros/{livro_id}")
def adicionar_livro(livro_id: int, livro: Livro = Body(...)):
    
    if livro_id in dicionario_livros:
        return {"message": "Livro com este ID já existe."}

    dicionario_livros[livro_id] = livro
    return {"message": "Livro adicionado com sucesso.", "livro": livro}

@app.get("/livros/{livro_id}")
def obter_livro(livro_id: int):

    if livro_id not in dicionario_livros:
        return {"message": "Livro não encontrado."}

    return {"livro": dicionario_livros[livro_id]}

@app.put("/livros/{livro_id}")
def atualizar_livro(livro_id: int, livro: Livro = Body(...)):

    if livro_id not in dicionario_livros:
        return {"message": "Livro não encontrado."}

    dicionario_livros[livro_id] = livro
    return {"message": "Livro atualizado com sucesso.", "livro": livro}


@app.patch("/livros/{livro_id}")
def atualizar_livro_parcial(livro_id: int, titulo: str = None, autor: str = None, ano: int = None):
    pass # implementação futura

@app.delete("/livros/{livro_id}")
def deletar_livro(livro_id: int):

    if livro_id not in dicionario_livros:
        return {"message": "Livro não encontrado."}

    del dicionario_livros[livro_id]
    return {"message": "Livro deletado com sucesso."}

disc_autores = {}

@app.get('/autores/')
def listar_autores(pag: int = 1, size: int = 2):
    pagina_inicial = (pag - 1) * size
    pagina_final = pagina_inicial + size

    ordem_autores = sorted(disc_autores.items(), key = lambda x: x[1].nome)

    autores_pag = []

    for id, autor in ordem_autores[pagina_inicial:pagina_final]:
        autor_dict = {
            "id": id,
            "nome": autor.nome,
            "idade": autor.idade
        }

        autores_pag.append(autor_dict)

    return {
        "page=": pag,
        "size=": size,
        "autores": autores_pag
        }
    

@app.post('/autores/{autor_id}')
def adicionar_autor(autor_id: int, autor: Autor = Body(...)):
    if autor_id in disc_autores:
        return {"message": "Autor com este ID já existe."}

    disc_autores[autor_id] = autor
    return {"message": "Autor adicionado com sucesso.", "autor": autor}


@app.get('/autores/filtro/')
def filtrar_autores(pag: int = 1, size: int = 2, filtar: str = "id"):

    if pag < 1 : 
        return { "erro": "Página deve ser mais 1"}


    pagina_inicial = (pag - 1) * size
    pagina_final = pagina_inicial + size


    if filtar == "nome": 
        ordem_autores = sorted(list(disc_autores.items()), key = lambda x: x[1].nome)

    elif filtar == "idade":
        ordem_autores = sorted(list(disc_autores.items()), key = lambda x: x[1].idade)

    elif filtar == "id":
        ordem_autores = sorted(list(disc_autores.items()), key = lambda x: x[0])
    else:
        return { "erro": "Filtro inválido. Use 'id', 'nome' ou 'idade'."}


    autores_pag = []

    for id, autor in ordem_autores[pagina_inicial:pagina_final]:
        autor_dict = {
            "id": id,
            "nome": autor.nome,
            "idade": autor.idade
        }

        autores_pag.append(autor_dict)

    return {
        "page=": pag,
        "size=": size,
        "autores": autores_pag,
        "paginacao": {
            "total_autores": len(disc_autores),
        }

    }



def autentica(credentials : HTTPBasicCredentials = Depends(HTTPBasic())):
   username = "admin"
   password = "senha123"
   if credentials.username != username or credentials.password != password:
         raise HTTPException(status_code=401, detail="Credenciais inválidas.")
   return credentials.username


disc_usuarios = {}
proximo_id_usuario = 1



@app.get('/usuarios/')
def listar_usuarios(username : str = Depends(autentica)):
    return {"usuario":disc_usuarios}



@app.post('/usuarios/')
def adicionar_usuario(
    usuario: Usuario = Body(...),
    username : str = Depends(autentica)
    ):


    global proximo_id_usuario

    disc_usuarios[proximo_id_usuario] = usuario
    proximo_id_usuario += 1
    return {"message": "Usuário adicionado com sucesso.", "usuario": usuario}
  