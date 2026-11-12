from flask import jsonify, redirect, render_template, request, session, url_for
from .forms import BuscaForm, CadastroForm, EdicaoForm
from .model import Item
from .app import app, db

@app.get("/language")
def set_language():
    language = request.args.get("language")
    if language in app.config.get("SUPPORTED_LOCALES", ("pt_BR", "en")):
        session["language"] = language

    next_url = request.args.get("next", url_for("pagina_cadastro"))
    if not next_url.startswith("/") or next_url.startswith("//"):
        next_url = url_for("pagina_cadastro")
    return redirect(next_url)

@app.route("/")
def pagina_cadastro():
    form = CadastroForm()
    return render_template("cadastro.html", form=form)

@app.route("/consulta")
def pagina_consulta():
    busca_form = BuscaForm()
    edicao_form = EdicaoForm()
    return render_template("consulta.html",
                            busca_form=busca_form,
                            edicao_form=edicao_form
                          )

"""
@app.route("/api/items", methods=["POST"])
def criar_item():
    dados = request.get_json()
    if not dados or not dados.get("nome"):
        return jsonify({"erro": "O campo 'nome' é obrigatório."}), 400

    if Item.query.filter_by(nome=dados["nome"].strip()).first():
        return jsonify({"erro": "Item já cadastrado."}), 409

    item = Item( nome=dados["nome"].strip(),
                 quantidade=int(dados.get("quantidade", 0)),
                 valor=float(dados.get("valor", 0.0)),
                )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201
"""

@app.route("/api/atualizar_item", methods=["POST"])
def atualizar_item():
    dados = request.get.json()
    if not dados:
        return jsonify({"erro": "Dados não enviados."}), 400
    item = db.session.get(Item, dados.get("id"))
    if item is None:
        return jsonify({"erro": "Item não encotrado."}), 400
    try:
        item.nome = dados["nome"]
        item.quantidade = int(dados["quantidade"])
        item.valor = float(dados["valor"])
        db.session.commit()
        
        return jsonify({ "mensagem": "Item atualizado com sucesso!"}), 200
    except (KeyError, TypeError, ValueError):
        db.session.rollback
        return jsonify({"erro": "Dados inválidos ou incompletos"}), 400