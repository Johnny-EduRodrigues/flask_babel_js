from .app import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    valor = db.Column(db.Float, nullable=False, default=0.0)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "quantidade": self.quantidade,
            "valor": self.valor,
        }
