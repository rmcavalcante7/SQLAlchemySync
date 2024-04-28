import sqlalchemy as sa
from datetime import datetime
from models.model_base import ModelBase
from sqlalchemy.exc import IntegrityError
from conf.db_session import createSession


class Ingrediente(ModelBase):
    __tablename__ = 'ingrediente'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True, autoincrement=True)
    nome: str = sa.Column(sa.String(45), unique=True, nullable=False)
    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)

    def __repr__(self):
        """Retorna uma representação do objeto em forma de 'string'."""
        return f'<Ingrediente (nome={self.nome})>'


def insertIngrediente(nome: str) -> Ingrediente or None:
    """Insere um Ingrediente na tabela ingrediente
    :param nome: str: nome do ingrediente
    :return: Ingrediente or None: Retorna o objeto Ingrediente se inserido com sucesso, None caso contrário
    :raises TypeError: Se o nome ou não for strings
    :raises RuntimeError: Se ocorrer um erro de integridade ao inserir o ingrediente, especificado para o nome. Caso
    seja por outro motivo, será lançado um erro genérico.
    """

    try:
        # check if is string
        if not isinstance(nome, str):
            raise TypeError('nome do Ingrediente deve ser uma string!')

        nome = nome.strip().upper()

        # validar se os parâmetros informados são válidos
        if not nome:
            raise ValueError('nome do Ingrediente não informado!')

        ingrediente = Ingrediente(nome=nome)

        with createSession() as session:
            print(f'Inserindo Ingrediente: {ingrediente}')
            session.add(ingrediente)
            session.commit()

            print(f'Ingrediente inserido com sucesso!')
            print(f'ID do Ingrediente inserido: {ingrediente.id}')
            print(f'Nome do Ingrediente inserido: {ingrediente.nome}')
            print(f'Data de criação do Ingrediente inserido: {ingrediente.data_criacao}')
        return ingrediente

    except IntegrityError as intg_error:
        if 'UNIQUE constraint failed' in str(intg_error):
            if 'ingrediente.nome' in str(intg_error):
                raise RuntimeError(f"Já existe um Ingrediente com o nome '{nome}' cadastrado. "
                                   f"O nome deve ser único.")
        else:
            # Tratar outros erros de integridade do SQLAlchemy
            raise RuntimeError(f'Erro de Ingrediente ao inserir ingrediente: {intg_error}')

    except TypeError as te:
        raise TypeError(te)

    except ValueError as ve:
        raise ValueError(ve)

    except Exception as exc:
        print(f'Erro inesperado: {exc}')


def selectAllIngredientes() -> list or []:
    """Seleciona todos os Ingredientes na tabela ingrediente
    :raises Exception: Informando erro inesperado
    :return: list or []: Retorna a lista de objetos Ingredientes se encontrados, [] caso contrário
    """
    try:
        with createSession() as session:
            ingredientes = session.query(Ingrediente).all()
            return ingredientes

    except Exception as exc:
        raise Exception(f'Erro inesperado ao selecionar Ingredientes: {exc}')


def selectIngredientePorId(id: int) -> Ingrediente or None:
    """Seleciona um Ingrediente na tabela ingrediente por id
    :param id: int: id do ingrediente
    :return: Ingrediente or None: Retorna o objeto Ingrediente se encontrado, None caso contrário
    :raises TypeError: Se o id não for um inteiro
    :raises ValueError: Se o id não for informado
    :return: Ingrediente or None: Retorna o objeto Ingrediente se encontrado, None caso contrário
    """
    try:
        # check if is integer
        if not isinstance(id, int):
            raise TypeError('id do Ingrediente deve ser um inteiro!')

        # validar se os parâmetros informados são válidos
        if not id:
            raise ValueError('id do Ingrediente não informado!')

        with createSession() as session:
            ingrediente = session.query(Ingrediente).filter(Ingrediente.id == id).first()
            return ingrediente

    except TypeError as te:
        raise TypeError(te)

    except ValueError as ve:
        raise ValueError(ve)

    except Exception as exc:
        print(f'Erro inesperado: {exc}')


def selectIngredientePorNome(nome: str) -> Ingrediente or None:
    """Seleciona um Ingrediente na tabela ingrediente por nome
    :param nome: str: nome do ingrediente
    :return: Ingrediente or None: Retorna o objeto Ingrediente se encontrado, None caso contrário
    :raises TypeError: Se o nome não for uma string
    :raises ValueError: Se o nome não for informado
    :return: Ingrediente or None: Retorna o objeto Ingrediente se encontrado, None caso contrário
    """
    try:
        # check if is string
        if not isinstance(nome, str):
            raise TypeError('nome do Ingrediente deve ser uma string!')

        nome = nome.strip().upper()

        # validar se os parâmetros informados são válidos
        if not nome:
            raise ValueError('nome do Ingrediente não informado!')

        with createSession() as session:
            ingrediente = session.query(Ingrediente).filter(Ingrediente.nome == nome).first()
            return ingrediente

    except TypeError as te:
        raise TypeError(te)

    except ValueError as ve:
        raise ValueError(ve)

    except Exception as exc:
        print(f'Erro inesperado: {exc}')


if __name__ == '__main__':
    try:
        insertIngrediente(nome='sal')
    except Exception as e:
        print(f'Erro ao inserir Ingrediente: {e}')

    try:
        insertIngrediente(nome='açúcar')
    except Exception as e:
        print(f'Erro ao inserir Ingrediente: {e}')

    try:
        insertIngrediente(nome='Leite')
    except Exception as e:
        print(f'Erro ao inserir Ingrediente: {e}')

    try:
        insertIngrediente(nome='Leite')
    except Exception as e:
        print(f'Erro ao inserir Ingrediente: {e}')

    try:
        insertIngrediente(nome='manga')
    except Exception as e:
        print(f'Erro ao inserir Ingrediente: {e}')

    try:
        insertIngrediente(nome='banana')
    except Exception as e:
        print(f'Erro ao inserir Ingrediente: {e}')
    print('fim')
