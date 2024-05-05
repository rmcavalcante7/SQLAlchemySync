import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from pathlib import Path  # usado no sqlite
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.future.engine import Engine
from models.model_base import ModelBase
from ScriptsAuxiliares.Auxiliar import Auxiliar


# Descrive all this module does
# This module is responsible for creating the connection to the database
# and creating the tables in the database.
# It also creates a session with the database to perform CRUD operations.
# the createEngine function is responsible for creating the connection to the database
# the createSession function is responsible for creating a session with the database
# the createTables function is responsible for creating the tables in the database
# the __engine variable is responsible for storing the connection to the database
# the __session variable is responsible for storing the session with the database
# This module is used in other modules to perform CRUD operations on the database
# This module is used in other modules to create the tables in the database
# This module is used in other modules to create a session with the database
# This module is used in other modules to create the connection to the database
# If the database already exists, the tables will be deleted and recreated


# This class will be used to create a session with the database and to
# define the connection to the database itself.
__engine: Optional[Engine] = None


def createEngine(sqlite: bool = True, echo: bool = False, timeout: int = 30) -> Engine:
    """Cria/Configura a engine de conexão com o banco de dados
    :param sqlite: bool: se True, usa o sqlite, se False, usa o postgres
    :param echo: bool: se True, mostra as queries executadas, se False, não mostra
    :param timeout: int: tempo limite para conexão, padrão 30 segundos
    :return: Engine
    """

    global __engine
    if __engine is not None:
        return __engine
    if sqlite:
        root_path = Auxiliar.getProjectRootDir()
        db_path = Path(f'{root_path}//db/picoles.sqlite')
        folder = Path(db_path).parent
        folder.mkdir(parents=True, exist_ok=True)
        conn_str = f'sqlite:///{db_path}'
        __engine = sa.create_engine(
            url=conn_str,  # caminho do banco de dados
            echo=echo,  # se True, mostra as queries executadas
            # fk on

            connect_args={
                "check_same_thread": False,  # para permitir multi-thread
                "timeout": timeout,  # tempo limite para conexão
            }
        )
    else:
        # opção para usar o postgres
        db_user_name = 'postgres'
        db_password = 'postgres'
        local = 'localhost'
        port = '5432'
        db_name = 'picoles'
        conn_str = f'postgresql://{db_user_name}:{db_password}@{local}:{port}/{db_name}'
        __engine = sa.create_engine(url=conn_str, echo=echo)
    return __engine


def createSession(sqlite: bool = True, echo: bool = False, timeout: int = 30) -> Session:
    """Cria uma sessão com o banco de dados para realizar operações de CRUD
    :param sqlite: bool: se True, usa o sqlite, se False, usa o postgres
    :param echo: bool: se True, mostra as queries executadas, se False, não mostra
    :param timeout: int: tempo limite para conexão, padrão 30 segundos
    :return: Session
    """

    global __engine
    if __engine is None:
        __engine = createEngine(sqlite=sqlite, echo=echo, timeout=timeout)

    __session = sessionmaker(bind=__engine, expire_on_commit=False, class_=Session)
    session: Session = __session()

    if sqlite:
        # ativa as chaves estrangeiras no sqlite, pois por padrão vem desativado,
        # caso contrário o sqlite não irá verificar se as chaves estrangeiras inseridas já existem e irá inserir
        # o registro mesmo que a chave estrangeira não exista
        session.execute('PRAGMA foreign_keys=ON;')
    return session


def createTables(sqlite: bool = True) -> None:
    """Cria as tabelas no banco de dados
    :param sqlite: bool: se True, usa o sqlite, se False, usa o postgres
    """

    global __engine
    if __engine is None:
        __engine = createEngine(sqlite=sqlite)

    ModelBase.metadata.drop_all(__engine)
    ModelBase.metadata.create_all(__engine)








