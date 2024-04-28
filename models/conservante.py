import sqlalchemy as sa
from datetime import datetime
from models.model_base import ModelBase
from conf.db_session import createSession
from sqlalchemy.exc import IntegrityError


class Conservante(ModelBase):
    __tablename__ = 'conservante'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True, autoincrement=True)
    nome: str = sa.Column(sa.String(45), unique=True, nullable=False)
    descricao: str = sa.Column(sa.String(45), nullable=False)
    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)

    def __repr__(self):
        """Retorna uma representação do objeto em forma de 'string'."""
        return f'<Conservante (nome={self.nome}, descrição={self.descricao})>'


def insertConservante(nome: str, descricao: str) -> Conservante or None:
    """Insere um Conservante na tabela conservante
    :param nome: str: nome do conservante
    :param descricao: str: fórmula química do conservante
    :return: Conservante or None: Retorna o objeto Conservante se inserido com sucesso, None caso contrário
    :raises TypeError: Se o nome ou a descrição não forem strings
    :raises ValueError: Se o nome ou a descrição não forem informados
    :raises RuntimeError: Se ocorrer um erro de integridade ao inserir o conservante, especificado para o nome. Caso
    seja por outro motivo, será lançado um erro genérico.
    """

    try:
        # check if is string
        if not isinstance(nome, str):
            raise TypeError('nome do Conservante deve ser uma string!')
        if not isinstance(descricao, str):
            raise TypeError('descricao do Conservante deve ser uma string!')

        nome = nome.strip().upper()
        descricao = descricao.strip().upper()

        # validar se os parâmetros informados são válidos
        if not nome:
            raise ValueError('nome do Conservante não informado!')
        if not descricao:
            raise ValueError('descricao do Conservante não informada!')

        conservante = Conservante(nome=nome, descricao=descricao)

        with createSession() as session:
            print(f'Inserindo Conservante: {conservante}')
            session.add(conservante)
            session.commit()

            print(f'Conservante inserido com sucesso!')
            print(f'ID do Conservante inserido: {conservante.id}')
            print(f'Nome do Conservante inserido: {conservante.nome}')
            print(f'Descrição do Conservante inserido: {conservante.descricao}')
            print(f'Data de criação do Conservante inserido: {conservante.data_criacao}')
        return conservante

    except IntegrityError as intg_error:
        if 'UNIQUE constraint failed' in str(intg_error):
            if 'conservante.nome' in str(intg_error):
                raise RuntimeError(f"Já existe um Conservante com o nome '{nome}' cadastrado. "
                                   f"O nome deve ser único.")
        else:
            # Tratar outros erros de integridade do SQLAlchemy
            raise RuntimeError(f'Erro de integridade ao inserir Conservante: {intg_error}')

    except TypeError as te:
        raise TypeError(te)

    except ValueError as ve:
        raise ValueError(ve)

    except Exception as exc:
        raise Exception(f'Erro inesperado ao selecionar todos Conservante: {exc}')


def selectAllConservantes() -> list or []:
    """Seleciona todos os Conservantes na tabela conservante
    :raises Exception: Informando erro inesperado ao selecionar os conservantes
    :return: list or []: Retorna uma lista de objetos Conservante se encontrado, [] caso contrário
    """
    try:
        with createSession() as session:
            conservantes = session.query(Conservante).all()
            return conservantes

    except Exception as exc:
        raise Exception(f'Erro inesperado ao selecionar Conservantes: {exc}')


def selectConservantePorID(id: int) -> Conservante or None:
    """Seleciona um Conservante na tabela conservante por ID
    :param id: int: id do Conservante
    :return: Conservante or None: Retorna o objeto Conservante se encontrado, None caso contrário
    :raises TypeError: Se o id não for um inteiro
    :raises ValueError: Se o id não for informado
    :raises RuntimeError: Se ocorrer um erro ao selecionar o conservante
    :return: Conservante or None: Retorna o objeto Conservante se encontrado, None caso contrário
    """

    try:
        # check if is int
        if not isinstance(id, int):
            raise TypeError('id do Conservante deve ser um inteiro!')

        # validar se o id informado é válido
        if not id:
            raise ValueError('id do Conservante não informado!')

        with createSession() as session:
            conservante = session.query(Conservante).filter(Conservante.id == id).first()
            return conservante

    except TypeError as te:
        raise TypeError(te)

    except ValueError as ve:
        raise ValueError(ve)

    except Exception as exc:
        print(f'Erro inesperado: {exc}')


def selectConservantePorNome(nome: str) -> Conservante or None:
    """Seleciona um Conservante na tabela conservante por nome
    :param nome: str: nome do Conservante
    :return: Conservante or None: Retorna o objeto Conservante se encontrado, None caso contrário
    :raises TypeError: Se o nome não for uma string
    :raises ValueError: Se o nome não for informado
    :raises RuntimeError: Se ocorrer um erro ao selecionar o conservante
    :return: Conservante or None: Retorna o objeto Conservante se encontrado, None caso contrário
    """

    try:
        # check if is string
        if not isinstance(nome, str):
            raise TypeError('nome do Conservante deve ser uma string!')

        nome = nome.strip().upper()

        # validar se o nome informado é válido
        if not nome:
            raise ValueError('nome do Conservante não informado!')

        with createSession() as session:
            conservante = session.query(Conservante).filter(Conservante.nome == nome).first()
            return conservante

    except TypeError as te:
        raise TypeError(te)

    except ValueError as ve:
        raise ValueError(ve)

    except Exception as exc:
        print(f'Erro inesperado: {exc}')


if __name__ == '__main__':
    try:
        insertConservante(nome='Sorbato de Potássio', descricao='Utilizado para conservar alimentos. '
                                                                'Evita a proliferação de fungos e leveduras.')
    except Exception as e:
        print(f'Erro ao inserir Conservante: {e}')

    try:
        insertConservante(nome='Benzoato de Sódio', descricao='Utilizado para conservar alimentos. '
                                                              'É útil para conservar alimentos ácidos, '
                                                              'como sucos de frutas.')
    except Exception as e:
        print(f'Erro ao inserir Conservante: {e}')
    print('fim')
