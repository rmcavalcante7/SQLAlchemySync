import sqlalchemy as sa
from datetime import datetime
from models.model_base import ModelBase
from conf.db_session import createSession
from sqlalchemy.exc import IntegrityError


class TipoPicole(ModelBase):
    __tablename__ = 'tipo_picole'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True, autoincrement=True)
    nome: str = sa.Column(sa.String(45), unique=True, nullable=False)
    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)

    def __repr__(self):
        """Retorna uma representação do objeto em forma de 'string'."""
        return f'<Tipo Picole(nome={self.nome})>'


def insertTipoPicole(nome: str) -> TipoPicole or None:
    """Insere um TipoPicole na tabela tipo_picole
    :param nome: str: nome do aditivo
    :return: TipoPicole or None: Retorna o objeto TipoPicole se inserido com sucesso, None caso contrário
    :raises TypeError: Se o nome ou a descrição não forem strings
    :raises ValueError: Se o nome ou a descrição não forem informados
    :raises RuntimeError: Se ocorrer um erro de integridade ao inserir o TipoPicole, especificado para o nome. Caso
    seja por outro motivo, será lançado um erro genérico.
    """

    try:
        # check if is string
        if not isinstance(nome, str):
            raise TypeError('nome do TipoPicole deve ser uma string!')

        nome = nome.strip().upper()

        # validar se os parâmetros informados são válidos
        if not nome:
            raise ValueError('nome do TipoPicole não informado!')

        tipo_picole = TipoPicole(nome=nome)
        with createSession() as session:
            print(f'Inserindo TipoPicole: {tipo_picole}')
            session.add(tipo_picole)
            session.commit()

        print(f'Tipo Picolé inserido com sucesso!')
        print(f'ID do TipoPicole inserido: {tipo_picole.id}')
        print(f'Nome TipoPicole inserido: {tipo_picole.nome}')
        print(f'Data de criação do TipoPicole inserido: {tipo_picole.data_criacao}')
        return tipo_picole

    except IntegrityError as intg_error:
        if 'UNIQUE constraint failed' in str(intg_error):
            if 'tipo_picole.nome' in str(intg_error):
                raise RuntimeError(f"Já existe um TipoPicole com o nome '{nome}' cadastrado. "
                                   f"O nome deve ser único.")
        else:
            # Tratar outros erros de integridade do SQLAlchemy
            raise RuntimeError(f'Erro de integridade ao inserir TipoPicole: {intg_error}')

    except TypeError as te:
        raise TypeError(te)

    except ValueError as ve:
        raise ValueError(ve)

    except Exception as exc:
        print(f'Erro inesperado: {exc}')


def selectAllTipoPicoles() -> list[TipoPicole] or []:
    """Retorna uma lista com todos os registros da tabela tipo_picole
    raises Exception: Informa erro inesperado ao selecionar TipoPicole
    :return: list[TipoPicole] or []: Retorna uma lista com os objetos TipoPicole encontrados, [] caso contrário
    """
    try:
        with createSession() as session:
            return session.query(TipoPicole).all()

    except Exception as exc:
        raise Exception(f'Erro inesperado ao selecionar todos TipoPicole: {exc}')


def selectTipoPicolePorId(id: int) -> TipoPicole or None:
    """Seleciona um TipoPicole na tabela tipo_picole por id
    :param id: int: id do TipoPicole a ser selecionado
    :return: TipoPicole or None: Retorna o objeto TipoPicole se encontrado, None caso contrário
    :raises TypeError: Se o id não for um inteiro
    :raises ValueError: Se o id não for informado
    :raises RuntimeError: Se ocorrer um erro de integridade ao selecionar o TipoPicole por id. Caso seja por outro
    motivo, será lançado um erro genérico.
    """
    try:
        # check if is string
        if not isinstance(id, int):
            raise TypeError('id do TipoPicole deve ser um inteiro!')

        # validar se os parâmetros informados são válidos
        if not id:
            raise ValueError('id do TipoPicole não informado!')

        with createSession() as session:
            tipo_picole = session.query(TipoPicole).filter(TipoPicole.id == id).first()
            if tipo_picole:
                return tipo_picole

    except TypeError as te:
        raise TypeError(te)

    except ValueError as ve:
        raise ValueError(ve)

    except Exception as exc:
        print(f'Erro inesperado: {exc}')


def selectTipoPicolePorNome(nome: str) -> TipoPicole or None:
    """Seleciona um TipoPicole na tabela tipo_picole por nome
    :param nome: str: nome do TipoPicole a ser selecionado
    :return: TipoPicole or None: Retorna o objeto TipoPicole se encontrado, None caso contrário
    :raises TypeError: Se o nome não for uma string
    :raises ValueError: Se o nome não for informado
    :raises RuntimeError: Se ocorrer um erro de integridade ao selecionar o TipoPicole por nome. Caso seja por outro
    motivo, será lançado um erro genérico.
    """
    try:
        # check if is string
        if not isinstance(nome, str):
            raise TypeError('nome do TipoPicole deve ser uma string!')

        nome = nome.strip().upper()
        # validar se os parâmetros informados são válidos
        if not nome:
            raise ValueError('nome do TipoPicole não informado!')

        with createSession() as session:
            tipo_picole = session.query(TipoPicole).filter(TipoPicole.nome == nome).first()
            if tipo_picole:
                return tipo_picole

        return None

    except TypeError as te:
        raise TypeError(te)

    except ValueError as ve:
        raise ValueError(ve)

    except Exception as exc:
        print(f'Erro inesperado: {exc}')


if __name__ == '__main__':
    try:
        insertTipoPicole(nome='Cremoso')
    except Exception as e:
        print(f'Erro ao inserir TipoPicole: {e}')

    try:
        insertTipoPicole(nome='Frutado')
    except Exception as e:
        print(f'Erro ao inserir TipoPicole: {e}')

    try:
        insertTipoPicole(nome='Frutado')
    except Exception as e:
        print(f'Erro ao inserir TipoPicole: {e}')
    print('fim')
