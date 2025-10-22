from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

class Livro(BaseModel):
    titulo: str
    autor: str
    ano: int

dicionario_livros = {}

@app.get("/")
def read_root():
    return {"message": "OK"}

@app.get("/livros/")
def listar_livros(pagina: int = 1, tamanho: int = 3):

    if not dicionario_livros:
        return {"message": "Nenhum livro cadastrado."}

    pagina_inicial = (pagina - 1) * tamanho
    #pag 1          = (1 - 1) * 5 = 0
    #pag 2          = (2 - 1) * 5 = 5
    #pag 3          = (3 - 1) * 5 = 10 
    #pag 4          = (4 - 1) * 5 = 15
    #pag 5          = (5 - 1) * 5 = 20
    #pag 6           = (6 - 1) * 5 = 25

    pagina_final = pagina_inicial + tamanho 

    livros_paginados = [
        {
            "id": livro_id,
            "titulo": livro.titulo,
            "autor": livro.autor,
            "ano": livro.ano
        } 
        for livro_id, livro in list(dicionario_livros.items())[pagina_inicial:pagina_final]
    ]
    

    return {
        "pagina": pagina,
        "tamanho de itens na pagina": tamanho,
        "livros": len(dicionario_livros),
        "livros": livros_paginados
    }

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