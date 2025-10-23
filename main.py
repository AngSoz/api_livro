from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

class Livro(BaseModel):
    titulo: str
    autor: str
    ano: int

class Autor(BaseModel):
    nome: str
    idade: int


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
def listar_autores():
    pass # implementação futura

@app.post('/autores/{autor_id}')
def adicionar_autor(autor_id: int, autor: Autor = Body(...)):
    pass # implementação futura