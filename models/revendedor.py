import sqlalchemy as sa
from datetime import datetime
from models.model_base import ModelBase
from conf.db_session import createSession
from sqlalchemy.exc import IntegrityError


class Revendedor(ModelBase):
    __tablename__ = 'revendedor'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True, autoincrement=True)
    nome: str = sa.Column(sa.String(100), nullable=False)
    cnpj: str = sa.Column(sa.String(14), unique=True, nullable=False)
    razao_social: str = sa.Column(sa.String(100), nullable=False)
    contato: str = sa.Column(sa.String(100), nullable=False)
    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)

    def __repr__(self):
        """Retorna uma representação do objeto em forma de 'string'."""
        return f'<Revendedor (nome={self.nome}, cnpj={self.cnpj}, razao_social={self.razao_social})>'

    @staticmethod
    def insertRevendedor(nome: str, cnpj: str, razao_social: str, contato: str) -> 'Revendedor' or None:
        """Insere um Revendedor na tabela revendedor
        :param nome: str: nome do revendedor
        :param cnpj: str: CNPJ do revendedor
        :param razao_social: str: razão social do revendedor
        :param contato: str: contato do revendedor
        :return: Revendedor or None: Retorna o objeto Revendedor se inserido com sucesso, None caso contrário
        :raises TypeError: Se o nome, cnpj, razao_social ou contato não forem strings
        :raises ValueError: Se o nome, cnpj, razao_social ou contato não forem informados
        :raises RuntimeError: Se ocorrer um erro de integridade ao inserir o revendedor, especificado para o cnpj. Caso
        seja por outro motivo, será lançado um erro genérico.
        """

        try:
            if not isinstance(nome, str):
                raise TypeError('nome do Revendedor deve ser uma string!')
            if not isinstance(cnpj, str):
                raise TypeError('cnpj do Revendedor deve ser uma string!')
            if not isinstance(razao_social, str):
                raise TypeError('razao_social do Revendedor deve ser uma string!')
            if not isinstance(contato, str):
                raise TypeError('contato do Revendedor deve ser uma string!')

            nome = nome.strip().upper()
            cnpj = cnpj.strip().upper()
            razao_social = razao_social.strip().upper()
            contato = contato.strip().upper()

            # validar se os parâmetros informados são válidos
            if not nome:
                raise ValueError('nome do Revendedor não informado!')
            if not cnpj:
                raise ValueError('cnpj do Revendedor não informado!')
            if len(cnpj) != 14:
                raise ValueError('cnpj do Revendedor deve ter 14 caracteres!')
            if not razao_social:
                raise ValueError('razao_social do Revendedor não informada!')
            if not contato:
                raise ValueError('contato do Revendedor não informado!')

            revendedor = Revendedor(nome=nome, cnpj=cnpj, razao_social=razao_social, contato=contato)
            with createSession() as session:
                print(f'Inserindo Revendedor: {revendedor}')
                session.add(revendedor)
                session.commit()

                print(f'Revendedor inserido com sucesso!')
                print(f'ID do Revendedor inserido: {revendedor.id}')
                print(f'Nome do Revendedor inserido: {revendedor.nome}')
                print(f'CPNJ do Revendedor inserido: {revendedor.cnpj}')
                print(f'Razão Social do Revendedor inserido: {revendedor.razao_social}')
                print(f'Contato do Revendedor inserido: {revendedor.contato}')
                print(f'Data de criação do Revendedor inserido: {revendedor.data_criacao}')
            return revendedor

        except IntegrityError as intg_error:
            if 'UNIQUE constraint failed' in str(intg_error):
                if 'revendedor.cnpj' in str(intg_error):
                    raise RuntimeError(f"Já existe um Revendedor com o CNPJ '{cnpj}' cadastrado. "
                                       f"O CNPJ deve ser único.")
            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de integridade ao inserir Revendedor: {intg_error}')

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectAllRevendedores() -> list['Revendedor'] or []:
        """Seleciona todos os Revendedores na tabela revendedor
        :return: list[Revendedor] or []: Retorna a lista de objetos Revendedor se encontrado, [] caso contrário
        :raises Exception: Informa erro inesperado ao selecionar Revendedores
        """
        try:
            with createSession() as session:
                revendedores = session.query(Revendedor).all()
                return revendedores

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar todos Revendedor: {exc}')

    @staticmethod
    def selectRevendedorPorId(id: int) -> 'Revendedor' or None:
        """Seleciona um Revendedor na tabela revendedor por id
        :param id: int: id do revendedor
        :return: Revendedor or None: Retorna o objeto Revendedor se encontrado, None caso contrário
        :raises TypeError: Se o id não for um inteiro
        :raises ValueError: Se o id não for informado
        """
        try:
            if not isinstance(id, int):
                raise TypeError('id do Revendedor deve ser um inteiro!')

            if not id:
                raise ValueError('id do Revendedor não informado!')

            with createSession() as session:
                revendedor = session.query(Revendedor).filter(Revendedor.id == id).first()
                return revendedor

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectRevendedorPorCnpj(cnpj: str) -> 'Revendedor' or None:
        """Seleciona um Revendedor na tabela revendedor por cnpj
        :param cnpj: str: CNPJ do revendedor
        :return: Revendedor or None: Retorna o objeto Revendedor se encontrado, None caso contrário
        :raises TypeError: Se o cnpj não for uma string
        :raises ValueError: Se o cnpj não for informado
        """
        try:
            if not isinstance(cnpj, str):
                raise TypeError('cnpj do Revendedor deve ser uma string!')

            cnpj = cnpj.strip().upper()

            if not cnpj:
                raise ValueError('cnpj do Revendedor não informado!')

            with createSession() as session:
                revendedor = session.query(Revendedor).filter(Revendedor.cnpj == cnpj).first()
                return revendedor

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectRevendedoresPorNome(nome: str) -> list['Revendedor'] or []:
        """Seleciona os Revendedore na tabela revendedor por nome
        :param nome: str: nome do revendedor
        :return: list[Revendedor] or []: Retorna a lista de objetos Revendedor se encontrado, [] caso contrário
        :raises TypeError: Se o nome não for uma string
        :raises ValueError: Se o nome não for informado
        """
        try:
            if not isinstance(nome, str):
                raise TypeError('nome do Revendedor deve ser uma string!')

            nome = nome.strip().upper()
            if not nome:
                raise ValueError('nome do Revendedor não informado!')

            with createSession() as session:
                revendedores = session.query(Revendedor).filter(Revendedor.nome == nome).first()
                return revendedores

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectRendedoresPorRaizSocial(razao_social: str) -> list['Revendedor'] or []:
        """Seleciona os Revendedore na tabela revendedor por razao_social
        :param razao_social: str: razao_social do revendedor
        :return: list[Revendedor] or []: Retorna a lista de objetos Revendedor se encontrado, [] caso contrário
        :raises TypeError: Se o razao_social não for uma string
        :raises ValueError: Se o razao_social não for informado
        """
        try:
            if not isinstance(razao_social, str):
                raise TypeError('razao_social do Revendedor deve ser uma string!')

            razao_social = razao_social.strip().upper()
            if not razao_social:
                raise ValueError('razao_social do Revendedor não informado!')

            with createSession() as session:
                revendedores = session.query(Revendedor).filter(Revendedor.razao_social == razao_social).first()
                return revendedores

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')


if __name__ == '__main__':
    try:
        Revendedor.insertRevendedor(nome='Sorbato de Potássio', cnpj='12345678901234',
                                    razao_social='Sorbato de Potássio LTDA',
                                    contato='Sorbato de Potássio')
    except Exception as e:
        print(f'Erro ao inserir Revendedor: {e}')

    try:
        Revendedor.insertRevendedor(nome='Benzoato de Sódio', cnpj='12345678901234',
                                    razao_social='Benzoato de Sódio LTDA',
                                    contato='Benzoato de Sódio')
    except Exception as e:
        print(f'Erro ao inserir Revendedor: {e}')

    print('fim')
