import pytest
from conf.db_session import createEngine, createTables
from sqlalchemy import inspect
from sqlalchemy.engine.base import Engine


@pytest.mark.order(1)
@pytest.fixture(scope="module")
def engine():
    engine = createEngine(sqlite=True)  # SQLite engine for testing
    yield engine
    engine.dispose()  # Close the connection after the test module finishes


def test_create_engine():
    # Verifica se a função createEngine retorna uma instância de Engine
    engine = createEngine(sqlite=True)
    assert isinstance(engine, Engine)


def test_database_connection(engine):
    # Verifica se a conexão com o banco de dados é bem-sucedida
    assert engine.connect()


def test_create_tables(engine):
    # Call createTables to create tables in the database
    createTables(sqlite=True)

    # Get the list of tables in the database
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    # Check if tables are created
    assert 'aditivo_nutritivo' in tables
    assert 'aditivo_nutritivo_picole' in tables
    assert 'conservante' in tables
    assert 'ingrediente' in tables
    assert 'ingrediente_picole' in tables
    assert 'lote_nota_fiscal' in tables
    assert 'nota_fiscal' in tables
    assert 'picole' in tables
    assert 'sabor' in tables
    assert 'tipo_embalagem' in tables
    assert 'tipo_picole' in tables


if __name__ == '__main__':
    pytest.main()
