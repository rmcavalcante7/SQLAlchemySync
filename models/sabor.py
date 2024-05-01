import sqlalchemy as sa
from datetime import datetime
from models.model_base import ModelBase
from conf.db_session import createSession
from sqlalchemy.exc import IntegrityError


class Sabor(ModelBase):
    __tablename__ = 'sabor'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True, autoincrement=True)
    nome: str = sa.Column(sa.String(45), unique=True, nullable=False)
    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)

    def __repr__(self):
        """Retorna uma representação do objeto em forma de 'string'."""
        return f'<Sabor(nome={self.nome})>'


    @staticmethod
    def insertSabor(nome: str) -> 'Sabor' or None:
        """Insere um Sabor na tabela sabor
        :param nome: str: nome do aditivo
        :return: Sabor or None: Retorna o objeto Sabor se inserido com sucesso, None caso contrário
        :raises TypeError: Se o nome não for string
        :raises ValueError: Se o nome não for informado
        :raises RuntimeError: Se ocorrer um erro de integridade ao inserir o sabor, especificado para o nome. Caso
        seja por outro motivo, será lançado um erro genérico.
        """

        try:
            # check if is string
            if not isinstance(nome, str):
                raise TypeError('nome do Sabor deve ser uma string!')

            nome = nome.strip().upper()

            # validar se os parâmetros informados são válidos
            if not nome:
                raise ValueError('nome do Sabor não informado!')

            sabor = Sabor(nome=nome)

            with createSession() as session:
                print(f'Inserindo Sabor: {sabor}')
                session.add(sabor)
                session.commit()

                print(f'Sabor inserido com sucesso!')
                print(f'ID do Sabor inserido: {sabor.id}')
                print(f'Nome do Sabor inserido: {sabor.nome}')
                print(f'Data de criação do Sabor inserido: {sabor.data_criacao}')
            return sabor

        except IntegrityError as intg_error:
            if 'UNIQUE constraint failed' in str(intg_error):
                if 'sabor.nome' in str(intg_error):
                    raise RuntimeError(f"Já existe um Sabor com o nome '{nome}' cadastrado. "
                                       f"O nome deve ser único.")
            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de integridade ao inserir sabor: {intg_error}')

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectAllSabores() -> list['Sabor'] or []:
        """Seleciona todos os Sabores na tabela sabor
        raises Exception: Informa erro inesperado ao selecionar Sabores
        :return: list[Sabor] or []: Retorna uma lista de objetos Sabor se houver registros, [] caso contrário
        """
        try:
            with createSession() as session:
                sabores = session.query(Sabor).all()
                return sabores
        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar todos Sabor: {exc}')

    @staticmethod
    def selectSaborPorId(id: int) -> 'Sabor' or None:
        """Seleciona um Sabor na tabela sabor por id
        :param id: int: id do Sabor
        :raises TypeError: Se o id não for um inteiro
        :raises ValueError: Se o id não for informado
        :return: Sabor or None: Retorna o objeto Sabor se encontrado, None caso contrário
        """
        try:
            if not isinstance(id, int):
                raise TypeError('id do Sabor deve ser um inteiro!')

            if not id:
                raise ValueError('id do Sabor não informado!')

            with createSession() as session:
                sabor = session.query(Sabor).filter(Sabor.id == id).first()
                return sabor

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar Sabor por id: {exc}')

    @staticmethod
    def selectSaborPorNome(nome: str) -> 'Sabor' or None:
        """Seleciona um Sabor na tabela sabor por nome
        :param nome: str: nome do Sabor
        :raises TypeError: Se o nome não for uma string
        :raises ValueError: Se o nome não for informado
        :return: Sabor or None: Retorna o objeto Sabor se encontrado, None caso contrário
        """
        try:
            if not isinstance(nome, str):
                raise TypeError('nome do Sabor deve ser uma string!')

            nome = nome.strip().upper()
            if not nome:
                raise ValueError('nome do Sabor não informado!')

            with createSession() as session:
                sabor = session.query(Sabor).filter(Sabor.nome == nome).first()
                return sabor

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar Sabor por nome: {exc}')


if __name__ == '__main__':
    try:
        Sabor.insertSabor(nome='Morango')
    except Exception as e:
        print(f'Erro ao inserir Sabor: {e}')

    try:
        Sabor.insertSabor(nome='Morango')
    except Exception as e:
        print(f'Erro ao inserir Sabor: {e}')

    try:
        Sabor.insertSabor(nome='Coco')
    except Exception as e:
        print(f'Erro ao inserir Sabor: {e}')

    print('fim')
