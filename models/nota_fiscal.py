import sqlalchemy as sa
import sqlalchemy.orm as orm
from datetime import datetime
from models.model_base import ModelBase
from models.revendedor import Revendedor
from models.lote import Lote
from typing import List
from conf.db_session import createSession
from sqlalchemy.exc import IntegrityError


class NotaFiscal(ModelBase):
    __tablename__ = 'nota_fiscal'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True, autoincrement=True)
    valor: float = sa.Column(sa.DECIMAL(decimal_return_scale=2), nullable=False)
    numero_serie: str = sa.Column(sa.String(45), unique=True, nullable=False)
    descricao: str = sa.Column(sa.String(200), nullable=False)

    revendedor_fk: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),
                                   sa.ForeignKey('revendedor.id'), nullable=False)
    revendedor: Revendedor = orm.relationship('Revendedor', lazy='joined')

    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)


    def __repr__(self):
        """Retorna uma representação do objeto em forma de 'string'."""
        return (f'<Nota Fiscal (numero_serie={self.numero_serie}, valor={self.valor},'
                f'descricao={self.descricao})>')



def insertNotaFiscal(valor: float, numero_serie: str, descricao: str, revendedor_fk: int) -> NotaFiscal or None:
    """Insere uma NotaFiscal na tabela nota_fiscal
    :param valor: float: valor da nota fiscal, duas casas decimais
    :param numero_serie: str: número de série da nota fiscal
    :param descricao: str: descrição da nota fiscal
    :param revendedor_fk: int: id do revendedor
    :return: NotaFiscal or None: Retorna o objeto NotaFiscal se inserido com sucesso, None caso contrário
    :raises TypeError: Se o valor não for um float, ou se o número de série ou a descrição não forem strings
    :raises ValueError: Se o valor, o número de série ou a descrição não forem informados
    :raises RuntimeError: Se ocorrer um erro de integridade ao inserir a nota fiscal, especificado para o número de série
    ou para o revendedor, caso já existam registros com esses valores. Caso seja por outr motivo, será lançado
    um erro genérico.
    """

    try:
        # check if is string
        if not isinstance(valor, float) and not isinstance(valor, int):
            raise TypeError('valor da NotaFiscal deve ser um número!')
        if not isinstance(numero_serie, str):
            raise TypeError('numero_serie da NotaFiscal deve ser uma string!')
        if not isinstance(descricao, str):
            raise TypeError('descricao da NotaFiscal deve ser uma string!')
        if not isinstance(revendedor_fk, int):
            raise TypeError('revendedor_fk da NotaFiscal deve ser um inteiro!')

        numero_serie = numero_serie.strip().upper()
        descricao = descricao.strip().upper()
        valor = round(float(valor), 2)

        if not numero_serie:
            raise ValueError('numero_serie da NotaFiscal não informado!')
        if not descricao:
            raise ValueError('descricao da NotaFiscal não informada!')


        nota_fiscal = NotaFiscal(valor=valor, numero_serie=numero_serie, descricao=descricao,
                                 revendedor_fk=revendedor_fk)
        # Verificar se já existe um registro com o nome e a fórmula informados
        with createSession() as session:
            print(f'Inserindo NotaFiscal: {nota_fiscal}')
            session.add(nota_fiscal)
            session.commit()

            print(f'Nota fiscal inserida com sucesso!')
            print(f'ID da NotaFiscal inserida: {nota_fiscal.id}')
            print(f'valor da NotaFiscal inserida: {nota_fiscal.valor}')
            print(f'numero_serie da NotaFiscal inserida: {nota_fiscal.numero_serie}')
            print(f'descricao da NotaFiscal inserida: {nota_fiscal.descricao}')
            print(f'revendedor_fk da NotaFiscal inserida: {nota_fiscal.revendedor_fk}')
            print(f'revendedor.nome da NotaFiscal inserida: {nota_fiscal.revendedor.nome}')
            return nota_fiscal
    except IntegrityError as intg_error:
        if 'UNIQUE constraint failed' in str(intg_error):
            if 'nota_fiscal.numero_serie' in str(intg_error):
                raise RuntimeError(f"Já existe uma Nota Fiscal com o número de série '{numero_serie}' cadastrado. "
                                   f"O número de série deve ser único.")
        elif 'FOREIGN KEY constraint failed' in str(intg_error):
            raise RuntimeError(f"""Erro de integridade ao inserir LoteNotaFiscal. 
                                    Verifique se a FK fornecida existe: {revendedor_fk=}"""
                               )
        else:
            raise RuntimeError(f'Erro de integridade ao inserir Nota Fiscal: {intg_error}')

    except TypeError as te:
        raise TypeError(te)

    except ValueError as ve:
        raise ValueError(ve)

    except Exception as exc:
        print(f'Erro inesperado: {exc}')


def selectAllNotasFiscal() -> List[NotaFiscal] or []:
    """Seleciona todas as Notas Fiscais na tabela nota_fiscal
    :return: List[NotaFiscal] or []: Retorna uma lista de objetos NotaFiscal se encontrados, [] caso contrário
    :raises Exception: Se ocorrer um erro inesperado ao selecionar Notas Fiscais
    """
    try:
        with createSession() as session:
            notas_fiscais = session.query(NotaFiscal).all()
            return notas_fiscais

    except Exception as e:
        raise Exception(f'Erro inesperado ao selecionar todas NotaFiscal: {e}')


def selectNotaFiscalPorId(id: int) -> NotaFiscal or None:
    """Seleciona uma Nota Fiscal na tabela nota_fiscal por id
    :param id: int: id da Nota Fiscal
    :return: NotaFiscal or None: Retorna o objeto NotaFiscal se encontrado, None caso contrário
    :raises TypeError: Se o id não for um inteiro
    :raises ValueError: Se o id não for informado
    :return: NotaFiscal or None: Retorna o objeto NotaFiscal se encontrado, None caso contrário
    """
    try:
        # check if is integer
        if not isinstance(id, int):
            raise TypeError('id da Nota Fiscal deve ser um inteiro!')

        # validar se os parâmetros informados são válidos
        if not id:
            raise ValueError('id da Nota Fiscal não informado!')

        with createSession() as session:
            nota_fiscal = session.query(NotaFiscal).filter(NotaFiscal.id == id).one_or_none()
            return nota_fiscal

    except TypeError as te:
        raise TypeError(te)

    except ValueError as ve:
        raise ValueError(ve)

    except Exception as exc:
        print(f'Erro inesperado: {exc}')


def selectNotaFiscalPorNumeroSerie(numero_serie: str) -> NotaFiscal or None:
    """Seleciona uma Nota Fiscal na tabela nota_fiscal por número de série
    :param numero_serie: str: número de série da Nota Fiscal
    :return: NotaFiscal or None: Retorna o objeto NotaFiscal se encontrado, None caso contrário
    :raises TypeError: Se o número de série não for uma string
    :raises ValueError: Se o número de série não for informado
    :return: NotaFiscal or None: Retorna o objeto NotaFiscal se encontrado, None caso contrário
    """
    try:
        # check if is string
        if not isinstance(numero_serie, str):
            raise TypeError('numero_serie da Nota Fiscal deve ser uma string!')

        # validar se os parâmetros informados são válidos
        numero_series = numero_serie.strip().upper()
        if not numero_serie:
            raise ValueError('numero_serie da Nota Fiscal não informado!')

        with createSession() as session:
            nota_fiscal = session.query(NotaFiscal).filter(NotaFiscal.numero_serie == numero_serie).one_or_none()
            return nota_fiscal

    except TypeError as te:
        raise TypeError(te)

    except ValueError as ve:
        raise ValueError(ve)

    except Exception as exc:
        print(f'Erro inesperado: {exc}')


def selectNotasFiscaisPorRevendedorFk(revendedor_fk: int) -> List[NotaFiscal] or []:
    """Seleciona Notas Fiscais na tabela nota_fiscal por revendedor_fk
    :param revendedor_fk: int: id do revendedor
    :return: List[NotaFiscal] or None: Retorna uma lista de objetos NotaFiscal se encontrado, None caso contrário
    :raises TypeError: Se o revendedor_fk não for um inteiro
    :raises ValueError: Se o revendedor_fk não for informado
    :return: List[NotaFiscal] or None: Retorna uma lista de objetos NotaFiscal se encontrado, None caso contrário
    """
    try:
        # check if is integer
        if not isinstance(revendedor_fk, int):
            raise TypeError('revendedor_fk da Nota Fiscal deve ser um inteiro!')

        # validar se os parâmetros informados são válidos
        if not revendedor_fk:
            raise ValueError('revendedor_fk da Nota Fiscal não informado!')

        with createSession() as session:
            notas_fiscais = session.query(NotaFiscal).filter(NotaFiscal.revendedor_fk == revendedor_fk).all()
            return notas_fiscais

    except TypeError as te:
        raise TypeError(te)

    except ValueError as ve:
        raise ValueError(ve)

    except Exception as exc:
        print(f'Erro inesperado: {exc}')



if __name__ == '__main__':
    try:
        insertNotaFiscal(valor=100.00, numero_serie='123456', descricao='Nota fiscal de teste', revendedor_fk=1)
    except Exception as e:
        print(f'Erro ao inserir Nota Fiscal: {e}')

    # repetido
    try:
        insertNotaFiscal(valor=100.00, numero_serie='123456', descricao='Nota fiscal de teste', revendedor_fk=1)
    except Exception as e:
        print(f'Erro ao inserir Nota Fiscal: {e}')

    # revendedor_fk não existe
    try:
        insertNotaFiscal(valor=100.00, numero_serie='123457', descricao='Nota fiscal de teste', revendedor_fk=1000)
    except Exception as e:
        print(f'Erro ao inserir Nota Fiscal: {e}')