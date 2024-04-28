import sqlalchemy as sa
import sqlalchemy.orm as orm
from datetime import datetime
from models.model_base import ModelBase
from models.sabor import Sabor
from models.tipo_picole import TipoPicole
from models.tipo_embalagem import TipoEmbalagem
from models.ingrediente import Ingrediente
from models.conservante import Conservante
from models.aditivo_nutritivo import AditivoNutritivo
from typing import List, Optional

# todo fazer um módulo para cada uma das tabelas abaixo
# Um picole pode ter vários ingredientes, relaciomaneto muitos para muitos
ingrediente_picole = sa.Table(
    'ingrediente_picole',  # Nome da tabela que será criada
    ModelBase.metadata,  # Metadados do banco de dados (SQLAlchemy), serve para criar a tabela
    sa.Column(
        'id',  # Nome da coluna
        sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
        primary_key=True,  # Chave primária
        autoincrement=True  # Autoincremento
    ),
    sa.Column(
        'picole_fk',  # Nome da coluna
        sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
        sa.ForeignKey('picole.id')  # Chave estrangeira para a tabela picole
    ),
    sa.Column(
        'ingrediente_fk',  # Nome da coluna
        sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
        sa.ForeignKey('ingrediente.id')  # Chave estrangeira para a tabela ingrediente
    )
)

# Um picole pode ter vários conservantes
conservante_picole = sa.Table(
    'conservante_picole',  # Nome da tabela que será criada
    ModelBase.metadata,  # Metadados do banco de dados (SQLAlchemy), serve para criar a tabela
    sa.Column(
        'id',  # Nome da coluna
        sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
        primary_key=True,  # Chave primária
        autoincrement=True  # Autoincremento
    ),
    sa.Column(
        'picole_fk',  # Nome da coluna
        sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
        sa.ForeignKey('picole.id')  # Chave estrangeira para a tabela picole
    ),
    sa.Column(
        'conservante_fk',  # Nome da coluna
        sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
        sa.ForeignKey('conservante.id')  # Chave estrangeira para a tabela conservante
    )
)

# Um pico pode ter vários aditivos nutritivos
aditivo_nutritivo_picole = sa.Table(
    'aditivo_nutritivo_picole',  # Nome da tabela que será criada
    ModelBase.metadata,  # Metadados do banco de dados (SQLAlchemy), serve para criar a tabela
    sa.Column(
        'id',  # Nome da coluna
        sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
        primary_key=True,  # Chave primária
        autoincrement=True  # Autoincremento
    ),
    sa.Column(
        'picole_fk',  # Nome da coluna
        sa.BigInteger,  # Tipo da coluna
        sa.ForeignKey('picole.id')
    ),  # Chave estrangeira para a tabela picole
    sa.Column(
        'aditivo_nutritivo_fk',
        sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
        sa.ForeignKey('aditivo_nutritivo.id')  # Chave estrangeira para a tabela aditivo_nutritivo
    )
)


class Picole(ModelBase):
    __tablename__ = 'picole'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True, autoincrement=True)
    preco: float = sa.Column(sa.DECIMAL(decimal_return_scale=2), nullable=False)

    sabor_fk: int = sa.Column(sa.BigInteger, sa.ForeignKey('sabor.id'), nullable=False)
    sabor: Sabor = orm.relationship('Sabor', lazy='joined')

    tipo_embalagem_fk: int = sa.Column(sa.BigInteger, sa.ForeignKey('tipo_embalagem.id'), nullable=False)
    tipo_embalagem: TipoEmbalagem = orm.relationship('TipoEmbalagem', lazy='joined')

    tipo_picole_fk: int = sa.Column(sa.BigInteger, sa.ForeignKey('tipo_picole.id'), nullable=False)
    tipo_picole: TipoPicole = orm.relationship('TipoPicole', lazy='joined')

    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)

    # um picole pode ter uma lista de ingredientes
    ingredientes: List[Ingrediente] = orm.relationship(
        'Ingrediente',  # utilizando a classe Ingrediente, que é a classe que representa a tabela ingrediente
        secondary=ingrediente_picole,  # tabela secundária que será criada
        backref='ingrediente',  # a tabela que esse relacionamento faz referência
        lazy='dynamic'  # carregamento dinâmico
    )

    # um picole pode ter uma lista de conservantes ou nenhum
    conservantes: Optional[List[Conservante]] = orm.relationship(
        'Conservante',  # utilizando a classe Conservante, que é a classe que representa a tabela conservante
        secondary=conservante_picole,  # tabela secundária que será criada
        backref='conservante',  # a tabela que esse relacionamento faz referência
        lazy='dynamic'  # carregamento dinâmico
    )

    # um picole pode ter uma lista de aditivos nutritivos ou nenhum
    aditivos_nutritivo: Optional[List[AditivoNutritivo]] = orm.relationship(
        'AditivoNutritivo',
        # utilizando a classe AditivoNutritivo, que é a classe que representa a tabela aditivo_nutritivo
        secondary=aditivo_nutritivo_picole,  # tabela secundária que será criada
        backref='aditivo_nutritivo',  # a tabela que esse relacionamento faz referência
        lazy='dynamic'
    )

    def __repr__(self):
        """Retorna uma representação do objeto em forma de 'string'."""
        return f'<Picole(nome={self.tipo_picole.nome}, sabor={self.sabor.nome}, preço={self.preco})>'
