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
    tipo_picole_fk: int = sa.Column(sa.BigInteger, sa.ForeignKey('tipo_picole.id'), nullable=False)
    # criando orm.relationship para acessar os dados da tabela relacionada,
    # é sempre necessário fazer essa configuração ao se ter uma chave estrangeira
    # permite acessar as informações da tabela relacionada, sem a necessidade de fazer uma nova consulta
    tipo_picole: TipoPicole = orm.relationship('TipoPicole', lazy='joined')

    quantidade: int = sa.Column(sa.BigInteger, nullable=False)
    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)

    def __repr__(self):
        """Retorna uma representação do objeto em forma de 'string'."""
        return f'<Lote (tipo_picole_fk={self.tipo_picole_fk}, quantidade={self.quantidade})>'


def insertLote(tipo_picole_fk: int, quantidade: int) -> Lote or None:
    """Insere um Lote na tabela lote
    :param tipo_picole_fk: int: id do tipo de picolé
    :param quantidade: int: quantidade de picolés do lote
    :return: Lote or None: Retorna o objeto Lote se inserido com sucesso, None caso contrário
    :raises TypeError: Se o nome ou não for strings
    :raises RuntimeError: Se ocorrer um erro de integridade ao inserir o lote, especificado para o tipo_picole_fk. Caso
    seja por outro motivo, será lançado um erro genérico.
    """

    try:
        # check if is string
        if not isinstance(tipo_picole_fk, int):
            raise TypeError('tipo_picole_fk deve ser um inteiro!')

        if not isinstance(quantidade, int):
            raise TypeError('quantidade deve ser um inteiro!')

        # validar se os parâmetros informados são válidos
        if quantidade <= 0:
            raise ValueError('quantidade de picolés do Lote deve ser maior que zero!')

        lote = Lote(tipo_picole_fk=tipo_picole_fk, quantidade=quantidade)

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
            raise RuntimeError(f"Erro de integridade ao inserir Lote: {tipo_picole_fk=} "
                               f"não encontrado!")
        else:
            raise RuntimeError(f'Erro de integridade ao inserir Lote: {intg_error}')

    except TypeError as te:
        raise TypeError(te)

    except ValueError as ve:
        raise ValueError(ve)

    except Exception as exc:
        print(f'Erro inesperado: {exc}')


if __name__ == '__main__':
    try:
        insertLote(tipo_picole_fk=1, quantidade=10)
    except Exception as e:
        print(f'Erro ao inserir Lote: {e}')
