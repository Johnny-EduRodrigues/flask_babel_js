from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, Length
from flask_babel import lazy_gettext as _

class CadastroForm(FlaskForm):
  nome = StringField(_("Nome"),
            validators=[DataRequired(message=_("O nome é obrigatório.")),
            Length(min=1, max=120, message=_("O nome deve ter entre 1 e 120 caracteres."))],
            render_kw={"placeholder": _("Nome do item")}
                    )
  quantidade = IntegerField(_("Quantidade"),
                               validators=[Optional(),   NumberRange(min=0, message="Valor mínimo: 0")],
                               default=0,
                               render_kw={"min": 0}
                             )
  valor = FloatField(_("Valor (R$)"),
                        validators=[Optional(), NumberRange(min=0.0, message="Valor mínimo: 0")],
                        default=0.0,
                        render_kw={"step": "0.01", "min": 0}
                    )
  submit = SubmitField(_("Cadastrar"))


class BuscaForm(FlaskForm):
    busca = StringField(_("Buscar item"),
              validators=[DataRequired(message=_("A busca é obrigatória.")), Length(min=3, message=_("Digite ao menos 3 letras"))],
              render_kw={"autocomplete": "off", "placeholder": _("Mínimo 3 letras")}
                        )


class EdicaoForm(FlaskForm):
    nome = StringField(_("Nome"),
                        validators=[DataRequired(message=_("O nome é obrigatório.")), Length(min=1, max=120, message=_("O nome deve ter entre 1 e 120 caracteres."))]
                      )
    quantidade = IntegerField(_("Quantidade"),
                              validators=[Optional(), NumberRange(min=0, message=_("Valor mínimo: 0"))],
                                render_kw={"min": 0}
                            )
    valor = FloatField(_("Valor (R$)"),
              validators=[Optional(), NumberRange(min=0.0, message=_("Valor mínimo: 0"))],
                        render_kw={"step": "0.01", "min": 0}
                      )
    submit_atualizar = SubmitField(_("Atualizar"))
    submit_deletar = SubmitField(_("Deletar"))
