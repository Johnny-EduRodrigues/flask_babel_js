
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import Schema, fields, validate
from flask_babel import gettext
from .model import Item
from .app import db

blp = Blueprint(
    "items",
    "items",
    url_prefix="/api/items",
    description="Operações RESTful sobre itens"
)


class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=120)
    )
    quantidade = fields.Int(load_default=0)
    valor = fields.Float(load_default=0.0)


class ItemUpdateSchema(Schema):
    nome = fields.Str(
        validate=validate.Length(min=1, max=120)
    )
    quantidade = fields.Int()
    valor = fields.Float()


class ItemQuerySchema(Schema):
    search = fields.Str(load_default="")


@blp.route("/")
class ListaItens(MethodView):

    @blp.arguments(ItemQuerySchema, location="query")
    @blp.response(200, ItemSchema(many=True))
    def get(self, args):
        termo = args.get("search", "").strip()

        if len(termo) < 3:
            return []

        return Item.query.filter(
            Item.nome.ilike(f"%{termo}%")
        ).all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item):
        novo_item = Item(
            nome=item["nome"],
            quantidade=item["quantidade"],
            valor=item["valor"]
        )

        db.session.add(novo_item)
        db.session.commit()

        return novo_item


@blp.route("/<int:item_id>")
class ItemTela(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        return Item.query.get_or_404(item_id)

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200)
    def put(self, dados, item_id):
        item = Item.query.get_or_404(item_id)

        if "nome" in dados:
            item.nome = dados["nome"]

        if "quantidade" in dados:
            item.quantidade = dados["quantidade"]

        if "valor" in dados:
            item.valor = dados["valor"]

        db.session.commit()

        return {"mensagem": gettext("Item atualizado com sucesso.")}

    @blp.response(200)
    def delete(self, item_id):
        item = Item.query.get_or_404(item_id)

        db.session.delete(item)
        db.session.commit()

        return {"mensagem": gettext("Item removido com sucesso.")}
