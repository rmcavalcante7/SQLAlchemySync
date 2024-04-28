import pytest
from models.tipo_picole import TipoPicole, insertTipoPicole


# @pytest.fixture
# def TipoPicole():
#     return TipoPicole(nome=nome)


nome = 'Aguado'

@pytest.mark.order(5)
# Teste criação de instancias de TipoPicole
def test_instancia_tipo_picole():
    tipo_picole = TipoPicole(nome=nome)
    assert tipo_picole.nome == nome


# Teste de inserção bem-sucedida
def test_inserir_tipo_picole():
    tipo_picole = insertTipoPicole(nome=nome)
    assert (tipo_picole.id is not None and
            tipo_picole.nome == nome.upper()
            )


# Teste de erro de integridade ao tentar inserir o mesmo registro duas vezes
def test_erro_integridade_mesma_combinacao():
    with pytest.raises(RuntimeError) as exc_info:
        insertTipoPicole(nome=nome)
    assert f"Já existe um TipoPicole com o nome '{nome.upper()}' cadastrado" in str(exc_info.value)


# Teste de erro ao inserir tipos de dados incorretos
def test_tipo_dados_incorretos():
    with pytest.raises(TypeError) as exc_info1:
        insertTipoPicole(nome=1)

    assert 'nome do TipoPicole deve ser uma string' in str(exc_info1.value)


# Teste de erro ao inserir valores vazios
def test_valores_vazios():
    with pytest.raises(ValueError) as exc_info1:
        insertTipoPicole(nome='')

    assert 'nome do TipoPicole não informado!' in str(exc_info1.value)


if __name__ == '__main__':
    pytest.main()

