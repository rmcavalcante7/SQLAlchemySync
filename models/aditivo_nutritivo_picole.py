import sqlalchemy as sa
import sqlalchemy.orm as orm
from datetime import datetime
from models.model_base import ModelBase
from models.picole import Picole
from models.aditivo_nutritivo import AditivoNutritivo
from conf.db_session import createSession
from sqlalchemy.exc import IntegrityError


class AditivoNutritivoPicole(ModelBase):
    __tablename__ = 'aditivo_nutritivo_picole'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True,
                        autoincrement=True)

    picole_fk: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),
                               sa.ForeignKey('picole.id'),
                               nullable=False
                               )
    picole: Picole = orm.relationship('Picole', lazy='joined')

    aditivo_nutritivo_fk: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),
                                          sa.ForeignKey('aditivo_nutritivo.id'),
                                          nullable=False
                                          )
    aditivo_nutritivo: AditivoNutritivo = orm.relationship('AditivoNutritivo', lazy='joined')

    # chave forte para impedir se ser inserido o mesmo par de lote e nota fiscal
    picole_aditivo_nutritivo: str = sa.Column(sa.String(200),
                                              unique=True,
                                              nullable=False)

    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)

    def __repr__(self):
        # return (f'AditivoNutritivoPicolePicole(id={self.id}, '
        #         f'picole_fk={self.picole_fk}, '
        #
        #         f'aditivo_nutritivo_fk={self.aditivo_nutritivo_fk}), '
        #         f'aditivo_nutritivo_nome={self.aditivo_nutritivo.nome})'
        #         )
        return (f"""
                    AditivoNutritivoPicole(
                      id={self.id}
                    , picole_fk={self.picole_fk}
                    {', picole.sabor=' + self.picole.sabor if self.picole else ''}                    
                    , aditivo_nutritivo_fk={self.aditivo_nutritivo_fk}
                    {', aditivo_nutritivo.nome=' + self.aditivo_nutritivo.nome if self.aditivo_nutritivo else ''}                    
                """
                )


    @staticmethod
    def insertAditivoNutritivoPicole(picole_fk: int, aditivo_nutritivo_fk: int) -> 'AditivoNutritivoPicole' or None:
        """Insere um AditivoNutritivoPicole na tabela aditivo_nutritivo_picole
        :param picole_fk: int: id do picolé
        :param aditivo_nutritivo_fk: int: id do aditivo nutritivo
        :return: AditivoNutritivoPicole or None: Retorna o objeto AditivoNutritivoPicole se inserido com sucesso, None caso contrário
        :raises TypeError: Se o picole_fk ou o aditivo_nutritivo_fk não forem inteiros
        :raises RuntimeError: Se as FKs picole_fk e aditivo_nutritivo_fk não existirem retorna um erro de integridade, caso
        contrário, retorna um erro genérico.
        """

        try:
            # check if is string
            if not isinstance(picole_fk, int):
                raise TypeError('picole_fk do AditivoNutritivoPicole deve ser um inteiro!')
            if not isinstance(aditivo_nutritivo_fk, int):
                raise TypeError('aditivo_nutritivo_fk do AditivoNutritivoPicole deve ser um inteiro!')


            aditivo_nutritivo_picole = AditivoNutritivoPicole(picole_fk=picole_fk,
                                                              aditivo_nutritivo_fk=aditivo_nutritivo_fk,
                                                              picole_aditivo_nutritivo=f'{picole_fk}-{aditivo_nutritivo_fk}'
                                                              )
            # Verificar se já existe um registro com o nome e a fórmula informados
            with createSession() as session:
                print(f'Inserindo AditivoNutritivoPicole: {aditivo_nutritivo_picole}')
                session.add(aditivo_nutritivo_picole)
                session.commit()

                print(f'Aditivo nutritivo inserido com sucesso!')
                print(f'ID do AditivoNutritivoPicole inserido: {aditivo_nutritivo_picole.id}')
                print(f'picole_fk do AditivoNutritivoPicole inserido: {aditivo_nutritivo_picole.picole_fk}')
                print(f'picole.sabor do AditivoNutritivoPicole inserido: {aditivo_nutritivo_picole.picole.sabor}')
                print(f'aditivo_nutritivo_fk do AditivoNutritivoPicole inserido: {aditivo_nutritivo_picole.aditivo_nutritivo_fk}')
                print(f'aditivo_nutritivo.nome do AditivoNutritivoPicole inserido: {aditivo_nutritivo_picole.aditivo_nutritivo.nome}')
            return aditivo_nutritivo_picole

        except IntegrityError as intg_error:
            if 'FOREIGN KEY constraint failed' in str(intg_error):
                raise RuntimeError(f"Erro de integridade ao inserir AditivoNutritivoPicole. "
                                   f"Verifique se as FKs fornecidas existem: "
                                   f"{picole_fk=} | {aditivo_nutritivo_fk=}"
                                   )
            elif 'UNIQUE constraint failed' in str(intg_error):
                raise RuntimeError(f"""Erro de integridade ao inserir AditivoNutritivoPicole. 
                Já existe um AditivoNutritivoPicole com a mesma combinação de picolé e aditivo nutritivo: {picole_fk=} | {aditivo_nutritivo_fk=}
                """)
            else:
                raise RuntimeError(f'Erro de integridade ao inserir Lote: {intg_error}')

        except TypeError as te:
            raise TypeError(te)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectAllAditivoNutritivoPicole() -> list['AditivoNutritivoPicole'] or []:
        """Seleciona todos os registros da tabela aditivo_nutritivo_picole
        :raises Exception: Informando erro inesperado ao selecionar os AditivoNutritivoPicole
        :return: List[AditivoNutritivoPicole]: Retorna uma lista de objetos AditivoNutritivoPicole
        """
        try:
            with createSession() as session:
                aditivo_nutritivo_picoles = session.query(AditivoNutritivoPicole).all()
                return aditivo_nutritivo_picoles

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar todos AditivoNutritivoPicole: {exc}')

    @staticmethod
    def selectAditivoNutritivoPorId(id: int) -> 'AditivoNutritivoPicole' or None:
        """Seleciona um AditivoNutritivoPicole na tabela aditivo_nutritivo_picole por ID
        :param id: int: id do AditivoNutritivoPicole
        :raises TypeError: Se o id não for um inteiro
        :raises ValueError: Se o id não for informado
        :raises RuntimeError: Se ocorrer um erro ao selecionar o AditivoNutritivoPicole
        :return: AditivoNutritivoPicole or None: Retorna o objeto AditivoNutritivoPicole se encontrado, None caso contrário
        """
        try:
            if not isinstance(id, int):
                raise TypeError('id do AditivoNutritivoPicole deve ser um inteiro!')
            if not id:
                raise ValueError('O id do AditivoNutritivoPicole deve ser informado!')

            with createSession() as session:
                aditivo_nutritivo_picole = session.query(AditivoNutritivoPicole).filter_by(id=id).first()
                return aditivo_nutritivo_picole

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise RuntimeError(f'Erro inesperado ao selecionar AditivoNutritivoPicole: {exc}')

    @staticmethod
    def selectAllAdiNutPicPorPicoleFK(picole_fk: int) -> list['AditivoNutritivoPicole'] or []:
        """Seleciona todos os AditivoNutritivoPicole na tabela aditivo_nutritivo_picole
        :param picole_fk: int: id do picolé
        :raises TypeError: Se o picole_fk não for um inteiro
        :raises Exception: Informando erro inesperado ao selecionar os AditivoNutritivoPicole
        :return: list or []: Retorna uma lista de objetos AditivoNutritivoPicole se encontrado, [] caso contrário
        """
        try:
            if not isinstance(picole_fk, int):
                raise TypeError('picole_fk do AditivoNutritivoPicole deve ser um inteiro!')
            with createSession() as session:
                aditivo_nutritivo_picoles = session.query(AditivoNutritivoPicole).filter_by(picole_fk=picole_fk).all()
                return aditivo_nutritivo_picoles

        except TypeError as te:
            raise TypeError(te)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar todos AditivoNutritivoPicole: {exc}')

    @staticmethod
    def selectAllAdiNutPicPorAditivoFK(aditivo_nutritivo_fk: int) -> list['AditivoNutritivoPicole'] or []:
        """Seleciona todos os AditivoNutritivoPicole na tabela aditivo_nutritivo_picole
        :param aditivo_nutritivo_fk: int: id do aditivo nutritivo
        :raises TypeError: Se o aditivo_nutritivo_fk não for um inteiro
        :raises Exception: Informando erro inesperado ao selecionar os AditivoNutritivoPicole
        :return: list or []: Retorna uma lista de objetos AditivoNutritivoPicole se encontrado, [] caso contrário
        """
        try:
            if not isinstance(aditivo_nutritivo_fk, int):
                raise TypeError('aditivo_nutritivo_fk do AditivoNutritivoPicole deve ser um inteiro!')

            with createSession() as session:
                aditivo_nutritivo_picoles = session.query(AditivoNutritivoPicole).filter_by(aditivo_nutritivo_fk=aditivo_nutritivo_fk).all()
                return aditivo_nutritivo_picoles

        except TypeError as te:
            raise TypeError(te)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar todos AditivoNutritivoPicole: {exc}')


if __name__ == '__main__':
    try:
        AditivoNutritivoPicole.insertAditivoNutritivoPicole(picole_fk=1, aditivo_nutritivo_fk=1)
    except Exception as e:
        print(f'Erro ao inserir AditivoNutritivoPicole: {e}')

    try:
        AditivoNutritivoPicole.insertAditivoNutritivoPicole(picole_fk=1, aditivo_nutritivo_fk=1)
    except Exception as e:
        print(f'Erro ao inserir AditivoNutritivoPicole: {e}')

    try:
        AditivoNutritivoPicole.insertAditivoNutritivoPicole(picole_fk=2, aditivo_nutritivo_fk=2)
    except Exception as e:
        print(f'Erro ao inserir AditivoNutritivoPicole: {e}')
