import sqlalchemy as sa
import sqlalchemy.orm as orm
from datetime import datetime
from models.model_base import ModelBase
from models.revendedor import Revendedor


class NotaFiscal(ModelBase):
    __tablename__ = 'nota_fiscal'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True, autoincrement=True)
    valor: float = sa.Column(sa.DECIMAL(decimal_return_scale=2), nullable=False)
    numero_serie: str = sa.Column(sa.String(45), unique=True, nullable=False)
    descricao: str = sa.Column(sa.String(200), nullable=False)

    revendedor_fk: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),
                                   sa.ForeignKey('revendedor.id'), nullable=False)
    revendedor: Revendedor = orm.relationship('Revendedor', lazy='joined')

    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)


    def __repr__(self):
        """Retorna uma representação do objeto em forma de 'string'."""
        return (f'<Nota Fiscal (numero_serie={self.numero_serie}, valor={self.valor},'
                f'descricao={self.descricao})>')

