import sqlalchemy as sa
from datetime import datetime
from models.model_base import ModelBase
from conf.db_session import createSession
from sqlalchemy.exc import IntegrityError


class AditivoNutritivo(ModelBase):
    """Classe que representa a tabela 'aditivo_nutritivo' no banco de dados.
    Atributos:
    - id: int: identificador do aditivo nutritivo
    - nome: str: nome do aditivo nutritivo, é único na tabela
    - formula_quimica: str: fórmula química do aditivo nutritivo, é única na tabela
    - data_criacao: datetime: data de criação do registro
    - data_atualizacao: datetime: data de atualização do registro
    """

    __tablename__ = 'aditivo_nutritivo'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True,
                        autoincrement=True,
                        nullable=False
                        )

    nome: str = sa.Column(sa.String(45),
                          unique=True,
                          nullable=False
                          )

    formula_quimica: str = sa.Column(sa.String(45),
                                     unique=True,
                                     nullable=False
                                     )

    data_criacao: datetime = sa.Column(sa.DateTime,
                                       default=datetime.now,
                                       nullable=False
                                       )

    data_atualizacao: datetime = sa.Column(sa.DateTime,
                                           default=datetime.now,
                                           onupdate=datetime.now,
                                           nullable=False
                                           )

    def __repr__(self):
        """Retorna uma representação do objeto em forma de 'string'."""
        return f'<Aditivo Nutritivo(nome={self.nome}, formula_quimica={self.formula_quimica})>'

    @staticmethod
    def insertAditivoNutritivo(nome: str, formula_quimica: str) -> 'AditivoNutritivo' or None:
        """Insere um AditivoNutritivo na tabela aditivos_nutritivos
        :param nome: str: nome do aditivo
        :param formula_quimica: str: fórmula química do aditivo
        :return: AditivoNutritivo or None: Retorna o objeto AditivoNutritivo se inserido com sucesso,
        None caso contrário
        :raises TypeError: Se o nome ou a fórmula química não forem strings
        :raises ValueError: Se o nome ou a fórmula química não forem informados
        :raises RuntimeError: Se ocorrer um erro de integridade ao inserir o aditivo nutritivo, especificado para o
        nome ou para a fórmula química, caso já existam registros com esses valores.
        Caso seja por outr motivo, será lançado um erro genérico.
        """

        try:
            # check if is string
            if not isinstance(nome, str):
                raise TypeError('nome do AditivoNutritivo deve ser uma string!')
            if not isinstance(formula_quimica, str):
                raise TypeError('formula_quimica do AditivoNutritivo deve ser uma string!')

            nome = nome.strip().upper()
            formula_quimica = formula_quimica.strip().upper()

            # validar se os parâmetros informados são válidos
            if not nome:
                raise ValueError('nome do AditivoNutritivo não informado!')
            if not formula_quimica:
                raise ValueError('formula_quimica do AditivoNutritivo não informada!')

            aditivo_nutritivo = AditivoNutritivo(nome=nome, formula_quimica=formula_quimica)
            # Verificar se já existe um registro com o nome e a fórmula informados
            with createSession() as session:
                # aditivo_existente = session.query(AditivoNutritivo).filter_by(
                #     nome=nome,
                #     formula_quimica=formula_quimica).first()
                #
                # if aditivo_existente:
                #     raise RuntimeError(f'Aditivo nutritivo {nome} com fórmula química {formula_quimica} já existe!')

                print(f'Inserindo AditivoNutritivo: {aditivo_nutritivo}')
                session.add(aditivo_nutritivo)
                session.commit()

                print(f'Aditivo nutritivo inserido com sucesso!')
                print(f'ID do AditivoNutritivo inserido: {aditivo_nutritivo.id}')
                print(f'Nome do AditivoNutritivo inserido: {aditivo_nutritivo.nome}')
                print(f'Fórmula química do AditivoNutritivo inserido: {aditivo_nutritivo.formula_quimica}')
                print(f'Data de criação do AditivoNutritivo inserido: {aditivo_nutritivo.data_criacao}')
            return aditivo_nutritivo

        except IntegrityError as intg_error:
            if 'UNIQUE constraint failed' in str(intg_error):
                if 'aditivo_nutritivo.nome' in str(intg_error):
                    raise RuntimeError(f"Já existe um AditivoNutritivo com o nome '{nome}' cadastrado. "
                                       f"O nome deve ser único.")
                elif 'aditivo_nutritivo.formula_quimica' in str(intg_error):
                    raise RuntimeError(
                        f"Já existe um AditivoNutritivo com a fórmula química '{formula_quimica}' cadastrada. "
                        f"A fórmula química deve ser única.")
            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de integridade ao inserir AditivoNutritivo: {intg_error}')

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectAditivoNutritivoPorId(id_aditivo_nutritivo: int) -> 'AditivoNutritivo' or None:
        """Seleciona um aditivo nutritivo cadastrado no banco de dados a partir do id.
        :param id_aditivo_nutritivo: int: identificador do aditivo nutritivo
        :raises TypeError: Se o id não for um inteiro
        :return: AditivoNutritivo or None: Retorna o objeto AditivoNutritivo se encontrado, None caso contrário
        """

        try:
            if not isinstance(id_aditivo_nutritivo, int):
                raise TypeError('id do AditivoNutritivo deve ser um inteiro!')

            # utilizando first: caso não encontre retorna None
            with createSession() as session:
                aditivo_nutritivo: AditivoNutritivo = session.query(AditivoNutritivo). \
                    filter_by(id=id_aditivo_nutritivo).first()

                return aditivo_nutritivo

            # Abaixo estão outras formas de fazer a mesma consulta, utilizando o one_or_none, one, where e first
            # utilizando o one_or_none: caso não encontre retorna None
            # with createSession() as session:
            #     aditivo_nutritivo: AditivoNutritivo = session.query(AditivoNutritivo).\
            #         filter_by(id=id_aditivo_nutritivo).one_or_none()
            #     return aditivo_nutritivo

            # utilizando o one: caso não encontre lança uma exceção
            # with createSession() as session:
            #     aditivo_nutritivo: AditivoNutritivo = session.query(AditivoNutritivo).\
            #         filter_by(id=id_aditivo_nutritivo).one()
            #     return aditivo_nutritivo

            # utilizando o where e first: caso não encontre retorna None
            # with createSession() as session:
            #     aditivo_nutritivo: AditivoNutritivo = session.query(AditivoNutritivo).\
            #         where(AditivoNutritivo.id == id_aditivo_nutritivo).first()
            #     return aditivo_nutritivo

            # utilizando o where e one_or_none: caso não encontre retorna None
            # with createSession() as session:
            #     aditivo_nutritivo: AditivoNutritivo = session.query(AditivoNutritivo).\
            #         where(AditivoNutritivo.id == id_aditivo_nutritivo).one_or_none()
            #     return aditivo_nutritivo

            # utilizando o where e one: caso não encontre lança uma exceção
            # with createSession() as session:
            #     aditivo_nutritivo: AditivoNutritivo = session.query(AditivoNutritivo).\
            #         where(AditivoNutritivo.id == id_aditivo_nutritivo).one()
            #     return aditivo_nutritivo
        except TypeError as te:
            raise TypeError(te)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar AditivoNutritivo: {exc}')

    @staticmethod
    def selectAditivoNutritivoPorNome(nome: str) -> 'AditivoNutritivo' or None:
        """Seleciona um aditivo nutritivo cadastrado no banco de dados a partir do nome.
        :param nome: str: nome do aditivo nutritivo
        :raises TypeError: Se o nome não for uma string
        :raises ValueError: Se o nome não for informado
        :return: AditivoNutritivo or None: Retorna o objeto AditivoNutritivo se encontrado, None caso contrário
        """
        try:
            if not isinstance(nome, str):
                raise TypeError('nome do AditivoNutritivo deve ser uma string!')

            nome = nome.strip().upper()
            if not nome:
                raise ValueError('nome do AditivoNutritivo não informado!')

            with createSession() as session:
                aditivo_nutritivo: AditivoNutritivo = session.query(AditivoNutritivo). \
                    filter_by(nome=nome).first()
                return aditivo_nutritivo

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar AditivoNutritivo: {exc}')

    @staticmethod
    def selectAditivoNutritivoPorFormulaQuimica(formula_quimica: str) -> 'AditivoNutritivo' or None:
        """Seleciona um aditivo nutritivo cadastrado no banco de dados a partir da fórmula química.
        :param formula_quimica: str: fórmula química do aditivo nutritivo
        :raises TypeError: Se a fórmula química não for uma string
        :raises ValueError: Se a fórmula química não for informada
        :return: AditivoNutritivo or None: Retorna o objeto AditivoNutritivo se encontrado, None caso contrário
        """
        try:
            if not isinstance(formula_quimica, str):
                raise TypeError('formula_quimica do AditivoNutritivo deve ser uma string!')

            formula_quimica = formula_quimica.strip().upper()
            if not formula_quimica:
                raise ValueError('formula_quimica do AditivoNutritivo não informada!')

            with createSession() as session:
                aditivo_nutritivo: AditivoNutritivo = session.query(AditivoNutritivo). \
                    filter_by(formula_quimica=formula_quimica).first()
                return aditivo_nutritivo

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar AditivoNutritivo: {exc}')

    @staticmethod
    def selectAllAditivosNutritivos() -> list['AditivoNutritivo'] or []:
        """Seleciona todos os aditivos nutritivos cadastrados no banco de dados.
        :raises Exception: Informando erro inesperado
        :return: list[AditivoNutritivo] or []: Retorna uma lista de objetos AditivoNutritivo se encontrados, [] caso contrário
        """
        try:
            with createSession() as session:
                aditivos_nutritivos: list[AditivoNutritivo] = session.query(AditivoNutritivo).all()
                return aditivos_nutritivos
        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar todos AditivoNutritivo: {exc}')

    @staticmethod
    def updateAditivoNutritivo(id_aditivo_nutritivo: int,
                               nome: str = '',
                               formula_quimica: str = '') -> 'AditivoNutritivo':
        """Atualiza um aditivo nutritivo cadastrado no banco de dados a partir do id.
        :param id_aditivo_nutritivo: int: identificador do aditivo nutritivo
        :param nome: str: caso se deseje atualizar o nome do aditivo nutritivo, informar o novo nome
        :param formula_quimica: str: caso se deseje atualizar a fórmula química do aditivo nutritivo,
                                    informar a nova fórmula
        :return: AditivoNutritivo: Retorna o objeto AditivoNutritivo atualizado
        :raises TypeError: Se o id não for um inteiro e não for informado
        :raises ValueError: Se o nome ou a fórmula química informados forem compostos só por espaços
        :raises RuntimeError: Se ocorrer um erro de integridade ao atualizar o aditivo nutritivo, especificado para o
        nome ou para a fórmula química, caso já existam registros com esses valores.
        """
        try:
            if not isinstance(id_aditivo_nutritivo, int):
                raise TypeError('id do AditivoNutritivo deve ser um inteiro!')

            if not isinstance(nome, str):
                raise TypeError('nome do AditivoNutritivo deve ser uma string!')

            if len(nome) > 0 and all(caractere.isspace() for caractere in nome):
                raise ValueError('nome do AditivoNutritivo não pode ser composto só por espaços!')

            if not isinstance(formula_quimica, str):
                raise TypeError('formula_quimica do AditivoNutritivo deve ser uma string!')

            if len(formula_quimica) > 0 and all(caractere.isspace() for caractere in formula_quimica):
                raise ValueError('formula_quimica do AditivoNutritivo não pode ser composta só por espaços!')

            nome = nome.strip().upper()
            formula_quimica = formula_quimica.strip().upper()

            with createSession(echo=True) as session:
                adititvo_nutritivo = session.query(AditivoNutritivo). \
                    filter_by(id=id_aditivo_nutritivo).first()

                if not adititvo_nutritivo:
                    raise ValueError(f'AditivoNutritivo com id={id_aditivo_nutritivo} não cadastrado na base!')


                adititvo_nutritivo.nome = nome.strip().upper() if nome.strip() else adititvo_nutritivo.nome

                adititvo_nutritivo.formula_quimica = formula_quimica.strip().upper() \
                    if formula_quimica.strip() else adititvo_nutritivo.formula_quimica

                adititvo_nutritivo.data_atualizacao = datetime.now()
                session.commit()
                return adititvo_nutritivo

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except IntegrityError as intg_error:
            if 'UNIQUE constraint failed' in str(intg_error):
                if 'aditivo_nutritivo.nome' in str(intg_error):
                    raise RuntimeError(f"Já existe um AditivoNutritivo com o nome '{nome}' cadastrado. "
                                       f"O nome deve ser único.")
                elif 'aditivo_nutritivo.formula_quimica' in str(intg_error):
                    raise RuntimeError(
                        f"Já existe um AditivoNutritivo com a fórmula química '{formula_quimica}' cadastrada. "
                        f"A fórmula química deve ser única.")
            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de integridade ao inserir AditivoNutritivo: {intg_error}')

        except Exception as exp:
            raise Exception(f'Erro inesperado ao atualizar AditivoNutritivo: {exp}')


if __name__ == '__main__':
    # try:
    #     insertAditivoNutritivo(nome='VITAMIna D', formula_quimica='C27H44O')
    # except Exception as e:
    #     print(f'Erro ao inserir AditivoNutritivo: {e}')
    #
    # # repetido
    # try:
    #     insertAditivoNutritivo(nome='VITAMIna D', formula_quimica='C27H44O')
    # except Exception as e:
    #     print(f'Erro ao inserir AditivoNutritivo: {e}')
    #
    # # inserir outro aditivo
    # try:
    #     insertAditivoNutritivo(nome='VITAMIna E', formula_quimica='C29H50O2')
    # except Exception as e:
    #     print(f'Erro ao inserir AditivoNutritivo: {e}')
    # print('fim')

    # selecionar aditivo por id
    # aditivo = AditivoNutritivo.selectAditivoNutritivoPorId(999)
    #
    # lista_aditivo_nutritivo = AditivoNutritivo.selectAllAditivosNutritivos()
    # for aditivo in lista_aditivo_nutritivo:
    #     print(f'Aditivo Nutritivo: '
    #           f'id={aditivo.id}, '
    #           f'nome={aditivo.nome}, '
    #           f'formula_quimica={aditivo.formula_quimica},'
    #           f'data_criacao={aditivo.data_criacao},'
    #           f'data_atualizacao={aditivo.data_atualizacao}'
    #           )

    aditivo_atualizado = AditivoNutritivo.updateAditivoNutritivo(id_aditivo_nutritivo=0,
                                                                 nome='VITAMINA C',
                                                                 formula_quimica='')
    print(aditivo_atualizado)
