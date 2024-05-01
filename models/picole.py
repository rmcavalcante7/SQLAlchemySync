import sqlalchemy as sa
import sqlalchemy.orm as orm
from datetime import datetime
from models.model_base import ModelBase
from models.sabor import Sabor
from models.tipo_picole import TipoPicole
from models.tipo_embalagem import TipoEmbalagem
from conf.db_session import createSession
from sqlalchemy.exc import IntegrityError


class Picole(ModelBase):
    __tablename__ = 'picole'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True, autoincrement=True)
    preco: float = sa.Column(sa.DECIMAL(decimal_return_scale=2), nullable=False)

    sabor_fk: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),
                              sa.ForeignKey('sabor.id'),
                              nullable=False)
    sabor: Sabor = orm.relationship('Sabor', lazy='joined')

    tipo_embalagem_fk: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),
                                       sa.ForeignKey('tipo_embalagem.id'),
                                       nullable=False)
    tipo_embalagem: TipoEmbalagem = orm.relationship('TipoEmbalagem', lazy='joined')

    tipo_picole_fk: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),
                                    sa.ForeignKey('tipo_picole.id'),
                                    nullable=False)
    tipo_picole: TipoPicole = orm.relationship('TipoPicole', lazy='joined')

    # chave forte para evitar duplicidades
    # chave forte para imedir se ser inserido o mesmo par de lote e nota fiscal
    sabor_tipoPicole_tipoEmbalagem: str = sa.Column(sa.String(200),
                                                    unique=True,
                                                    nullable=False)

    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)

    def __repr__(self):
        """Retorna uma representação do objeto em forma de 'string'."""
        return (f"""
                    Picole(
                        id={self.id}
                        , preço={self.preco} 
                        {', picole.sabor=' + self.tipo_picole.nome if self.tipo_picole else ''}   
                        {', picole.sabor=' + self.sabor.nome if self.sabor else ''}                                     
                        )"""
                )


    @staticmethod
    def insertPicole(preco: float, sabor_fk: int, tipo_embalagem_fk: int, tipo_picole_fk: int) -> 'Picole' or None:
        """Insere um Picole na tabela picole
        :param preco: float: preço do picolé
        :param sabor_fk: int: id do sabor
        :param tipo_embalagem_fk: int: id do tipo de embalagem
        :param tipo_picole_fk: int: id do tipo de picolé
        :return: Picole or None: Retorna o objeto Picole se inserido com sucesso, None caso contrário
        :raises TypeError: Se o preço não for float
        :raises ValueError: Se o preço não for informado
        :raises RuntimeError: Se as FKs sabor_fk, tipo_embalagem_fk e tipo_picole_fk não existirem retorna um erro de
        integridade, caso contrário, retorna um erro genérico.
        """

        try:
            # check if is string
            if not isinstance(preco, float) and not isinstance(preco, int):
                raise TypeError('preco do Picole deve ser numérico!')

            # check if is string
            if not isinstance(sabor_fk, int):
                raise TypeError('sabor_fk do Picole deve ser um inteiro!')

            # check if is string
            if not isinstance(tipo_embalagem_fk, int):
                raise TypeError('tipo_embalagem_fk do Picole deve ser um inteiro!')

            # check if is string
            if not isinstance(tipo_picole_fk, int):
                raise TypeError('tipo_picole_fk do Picole deve ser um inteiro!')

            preco = float(preco)

            picole = Picole(preco=preco, sabor_fk=sabor_fk, tipo_embalagem_fk=tipo_embalagem_fk,
                            tipo_picole_fk=tipo_picole_fk)
            picole.sabor_tipoPicole_tipoEmbalagem = f'{picole.sabor_fk}_{picole.tipo_picole_fk}_{picole.tipo_embalagem_fk}'
            with createSession() as session:
                print(f'Inserindo Picole: {picole}')
                session.add(picole)
                session.commit()

                print(f'Picole inserido com sucesso!')
                print(f'ID do Pciole inserido: {picole.id}')
                print(f'preco do Picole inserido: {picole.preco}')
                print(f'sabor do Picole inserido: {picole.sabor.nome}')
                print(f'tipo_embalagem do Picole inserido: {picole.tipo_embalagem.nome}')
                print(f'tipo_picole do Picole inserido: {picole.tipo_picole.nome}')

            return picole
        except IntegrityError as e:
            if 'FOREIGN KEY constraint failed' in str(e):
                raise RuntimeError(f"""Erro de integridade ao inserir Picole. Verifique se as FKs fornecidas existem: {sabor_fk=} | {tipo_embalagem_fk=} | {tipo_picole_fk=}"""
                                   )
            elif 'UNIQUE constraint failed' in str(e):
                raise RuntimeError(f"""Erro de integridade ao inserir Picole. Já existe um Picole com a mesma combinação de sabor_fk, tipo_picole_fk e tipo_embalagem_fk: {sabor_fk=} | {tipo_picole_fk=} | {tipo_embalagem_fk=}"""
                                   )
            else:
                raise RuntimeError(f'Erro de integridade ao inserir Picole: {e}')

        except TypeError as te:
            raise TypeError(te)

        except Exception as e:
            print(f'Erro inesperado: {e}')

    @staticmethod
    def selectAllPicoles() -> list['Picole'] or []:
        """Seleciona todos os Picoles na tabela picole
        :raises Exception: Informa erro inesperado ao selecionar Picoles
        :return: list[Picole] or []: Retorna uma lista de objetos Picole se encontrado, [] caso contrário
        """
        try:
            with createSession() as session:
                picoles = session.query(Picole).all()
                return picoles

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar todos Picole: {exc}')

    @staticmethod
    def selectPicolePorId(id: int) -> 'Picole' or None:
        """Seleciona um Picole na tabela picole por id
        :param id: int: id do picolé
        :return: Picole or None: Retorna o objeto Picole se encontrado, None caso contrário
        :raises TypeError: Se o id não for um inteiro
        :raises ValueError: Se o id não for informado
        :return: Picole or None: Retorna o objeto Picole se encontrado, None caso contrário
        """
        try:
            if not isinstance(id, int):
                raise TypeError('id do Picole deve ser um inteiro!')

            # validar se os parâmetros informados são válidos
            if not id:
                raise ValueError('id do Picole não informado!')

            with createSession() as session:
                picole = session.query(Picole).filter(Picole.id == id).first()
                return picole

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectPicolePorSabor(sabor_fk: int) -> list['Picole'] or []:
        """Seleciona Picoles na tabela picole por sabor
        :param sabor_fk: int: id do sabor
        :raises TypeError: Se o sabor_fk não for um inteiro
        :raises ValueError: Se o sabor_fk não for informado
        :return: list[Picole] or []: Retorna uma lista de objetos Picole se encontrado, [] caso contrário
        """
        try:
            if not isinstance(sabor_fk, int):
                raise TypeError('sabor_fk do Picole deve ser um inteiro!')

            # validar se os parâmetros informados são válidos
            if not sabor_fk:
                raise ValueError('sabor_fk do Picole não informado!')

            with createSession() as session:
                picoles = session.query(Picole).filter(Picole.sabor_fk == sabor_fk).all()
                return picoles

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectPicolesPorTipoEmbalagem(tipo_embalagem_fk: int) -> list['Picole'] or []:
        """Seleciona Picoles na tabela picole por tipo de embalagem
        :param tipo_embalagem_fk: int: id do tipo de embalagem
        :raises TypeError: Se o tipo_embalagem_fk não for um inteiro
        :raises ValueError: Se o tipo_embalagem_fk não for informado
        :return: list[Picole] or []: Retorna uma lista de objetos Picole se encontrado, [] caso contrário
        """
        try:
            if not isinstance(tipo_embalagem_fk, int):
                raise TypeError('tipo_embalagem_fk do Picole deve ser um inteiro!')

            # validar se os parâmetros informados são válidos
            if not tipo_embalagem_fk:
                raise ValueError('tipo_embalagem_fk do Picole não informado!')

            with createSession() as session:
                picoles = session.query(Picole).filter(Picole.tipo_embalagem_fk == tipo_embalagem_fk).all()
                return picoles

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectPicolesPorTipoPicole(tipo_picole_fk: int) -> list['Picole'] or []:
        """Seleciona Picoles na tabela picole por tipo de picolé
        :param tipo_picole_fk: int: id do tipo de picolé
        :raises TypeError: Se o tipo_picole_fk não for um inteiro
        :raises ValueError: Se o tipo_picole_fk não for informado
        :return: list[Picole] or []: Retorna uma lista de objetos Picole se encontrado, [] caso contrário
        """
        try:
            if not isinstance(tipo_picole_fk, int):
                raise TypeError('tipo_picole_fk do Picole deve ser um inteiro!')

            # validar se os parâmetros informados são válidos
            if not tipo_picole_fk:
                raise ValueError('tipo_picole_fk do Picole não informado!')

            with createSession() as session:
                picoles = session.query(Picole).filter(Picole.tipo_picole_fk == tipo_picole_fk).all()
                return picoles

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')


if __name__ == '__main__':
    try:
        Picole.insertPicole(preco=1.5, sabor_fk=1, tipo_embalagem_fk=1, tipo_picole_fk=1)
    except Exception as e:
        print(f'Erro ao inserir Picole: {e}')

    try:
        Picole.insertPicole(preco=1.5, sabor_fk=1, tipo_embalagem_fk=1, tipo_picole_fk=1)
    except Exception as e:
        print(f'Erro ao inserir Picole: {e}')

    try:
        Picole.insertPicole(preco=1.5, sabor_fk=1, tipo_embalagem_fk=1, tipo_picole_fk=2)
    except Exception as e:
        print(f'Erro ao inserir Picole: {e}')
