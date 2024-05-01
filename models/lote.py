from typing import Union

import sqlalchemy as sa
import sqlalchemy.orm as orm
from datetime import datetime
from models.model_base import ModelBase
from models.tipo_picole import TipoPicole
from sqlalchemy.exc import NoForeignKeysError, IntegrityError
from conf.db_session import createSession


class Lote(ModelBase):
    __tablename__ = 'lote'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True, autoincrement=True)

    # fk: nome_tabela.nome_campo
    picole_fk: int = sa.Column(sa.BigInteger, sa.ForeignKey('picole.id'), nullable=False)
    # criando orm.relationship para acessar os dados da tabela relacionada,
    # é sempre necessário fazer essa configuração ao se ter uma chave estrangeira
    # permite acessar as informações da tabela relacionada, sem a necessidade de fazer uma nova consulta
    picole: TipoPicole = orm.relationship('Picole', lazy='joined')

    quantidade: int = sa.Column(sa.BigInteger, nullable=False)
    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)

    def __repr__(self):
        """Retorna uma representação do objeto em forma de 'string'."""
        return f'<Lote (picole_fk={self.tipo_picole_fk}, quantidade={self.quantidade})>'


    @staticmethod
    def insertLote(picole_fk: int, quantidade: int) -> 'Lote' or None:
        """Insere um Lote na tabela lote
        :param picole_fk: int: id do picolé
        :param quantidade: int: quantidade de picolés do lote
        :return: Lote or None: Retorna o objeto Lote se inserido com sucesso, None caso contrário
        :raises TypeError: Se o nome ou não for strings
        :raises RuntimeError: Se ocorrer um erro de integridade ao inserir o lote, especificado para o tipo_picole_fk. Caso
        seja por outro motivo, será lançado um erro genérico.
        """

        try:
            # check if is string
            if not isinstance(picole_fk, int):
                raise TypeError('picole_fk deve ser um inteiro!')

            if not isinstance(quantidade, int):
                raise TypeError('quantidade deve ser um inteiro!')

            # validar se os parâmetros informados são válidos
            if quantidade <= 0:
                raise ValueError('quantidade de picolés do Lote deve ser maior que zero!')

            lote = Lote(picole_fk=picole_fk, quantidade=quantidade)

            with createSession() as session:
                print(f'Inserindo lote: {lote}')
                session.add(lote)
                session.commit()

                print(f'Lote inserido com sucesso!')
                print(f'ID do Lote inserido: {lote.id}')
                print(f'Nome do Tipo de picolé do Lote inserido: {lote.tipo_picole}')
                print(f'Quantidade de picolé do Lote inserido: {lote.quantidade}')
                return lote

        except IntegrityError as intg_error:
            if 'FOREIGN KEY constraint failed' in str(intg_error):
                raise RuntimeError(f"Erro de integridade ao inserir Lote: {picole_fk=} "
                                   f"não encontrado!")
            else:
                raise RuntimeError(f'Erro de integridade ao inserir Lote: {intg_error}')

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectAllLotes() -> list['Lote'] or []:
        """Seleciona todos os Lotes na tabela lote
        :raises Exception: Informa erro inesperado ao selecionar Lotes
        :return: list[Lote] or []: Retorna uma lista de objetos Lote se encontrado, [] caso contrário
        """
        try:
            with createSession() as session:
                lotes = session.query(Lote).all()
                return lotes

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar todos Lote: {exc}')


    @staticmethod
    def selectLotePorId(id: int) -> 'Lote' or None:
        """Seleciona um Lote na tabela lote por id
        :param id: int: id do lote
        :raises TypeError: Se o id não for um inteiro
        :raises ValueError: Se o id não for informado
        :return: Lote or None: Retorna o objeto Lote se encontrado, None caso contrário
        """
        try:

            if not isinstance(id, int):
                raise TypeError('id do Lote deve ser um inteiro!')

            # validar se os parâmetros informados são válidos
            if not id:
                raise ValueError('id do Lote não informado!')

            with createSession() as session:
                lote = session.query(Lote).filter(Lote.id == id).one_or_none()
                return lote

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as e:
            print(f'Erro ao selecionar Lote: {e}')


    @staticmethod
    def selectLotesPorPicoleFk(picole_fk: int) -> list['Lote'] or []:
        """Seleciona um Lote na tabela lote por picole_fk
        :param picole_fk: int: id do picolé
        :raises TypeError: Se o picole_fk não for um inteiro
        :raises ValueError: Se o picole_fk não for informado
        :return: list[Lote] or []: Retorna uma lista de objetos Lote se encontrado, [] caso contrário
        """
        try:
            if not isinstance(picole_fk, int):
                raise TypeError('picole_fk do Lote deve ser um inteiro!')

            # validar se os parâmetros informados são válidos
            if not picole_fk:
                raise ValueError('picole_fk do Lote não informado!')

            with createSession() as session:
                lotes = session.query(Lote).filter(Lote.picole_fk == picole_fk).all()
                return lotes

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro ao selecionar Lote: {exc}')


    @staticmethod
    def updateLote(id_lote: int, picole_fk: Union[int, None], quantidade: Union[int, None]) -> 'Lote':
        """Atualiza um Lote na tabela lote
        :param id_lote: int: id do lote
        :param picole_fk: int: id do picolé
        :param quantidade: int: quantidade de picolés do lote
        :return: Lote: Retorna o objeto Lote se atualizado com sucesso
        :raises TypeError: Se o id, picole_fk ou quantidade não for um inteiro
        :raises ValueError: Se o id, picole_fk ou quantidade não for informado
        :raises RuntimeError: Se ocorrer um erro de integridade ao atualizar o lote, especificado para o tipo_picole_fk. Caso
        seja por outro motivo, será lançado um erro genérico.
        """
        try:
            if not isinstance(id_lote, int):
                raise TypeError('id_lote do Lote deve ser um inteiro!')

            if not isinstance(picole_fk, int) and picole_fk is not None:
                raise TypeError('picole_fk do Lote deve ser um inteiro ou não deve ser informado!')

            if not isinstance(quantidade, int) and quantidade is not None:
                raise TypeError('quantidade do Lote deve ser um inteiro ou não deve ser informado!')

            if quantidade is not None and quantidade <= 0:
                raise ValueError('quantidade de picolés do Lote deve ser maior que zero!')

            with createSession() as session:
                lote = session.query(Lote).filter_by(id=id_lote).first()

                if not lote:
                    raise ValueError(f'Ingrediente com id={id_lote} não cadastrado na base!')

                if picole_fk:
                    lote.picole_fk = picole_fk
                else:
                    picole_fk = lote.picole_fk

                if quantidade:
                    lote.quantidade = quantidade

                session.commit()
                return lote

        except IntegrityError as intg_error:
            if 'FOREIGN KEY constraint failed' in str(intg_error):
                raise RuntimeError(f"Erro de integridade ao inserir Lote: {picole_fk=} "
                                   f"não encontrado!")
            else:
                raise RuntimeError(f'Erro de integridade ao inserir Lote: {intg_error}')

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao atualizar Lote: {exc}')


if __name__ == '__main__':
    # try:
    #     Lote.insertLote(picole_fk=1, quantidade=10)
    # except Exception as e:
    #     print(f'Erro ao inserir Lote: {e}')

    lote = Lote.updateLote(id_lote=1,
                           picole_fk=1,
                           quantidade=0)
    print(f'Lote atualizado: {lote}')