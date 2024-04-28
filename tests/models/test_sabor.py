import pytest
from models.sabor import Sabor, insertSabor


# @pytest.fixture
# def Sabor():
#     return Sabor(nome=nome)


nome = 'asdf'

@pytest.mark.order(7)

# Teste criação de instancias de Sabor
def test_instancia_sabor():
    sabor = Sabor(nome=nome)
    assert sabor.nome == nome


# Teste de inserção bem-sucedida
def test_inserir_sabor():
    sabor = insertSabor(nome=nome)
    assert (sabor.id is not None and
            sabor.nome == nome.upper()
            )


# Teste de erro de integridade ao tentar inserir o mesmo registro duas vezes
def test_erro_integridade_mesma_combinacao():
    with pytest.raises(RuntimeError) as exc_info:
        insertSabor(nome=nome)
    assert f"Já existe um Sabor com o nome '{nome.upper()}' cadastrado" in str(exc_info.value)


# Teste de erro ao inserir tipos de dados incorretos
def test_tipo_dados_incorretos():
    with pytest.raises(TypeError) as exc_info1:
        insertSabor(nome=1)

    assert 'nome do Sabor deve ser uma string' in str(exc_info1.value)


# Teste de erro ao inserir valores vazios
def test_valores_vazios():
    with pytest.raises(ValueError) as exc_info1:
        insertSabor(nome='')

    assert 'nome do Sabor não informado!' in str(exc_info1.value)


if __name__ == '__main__':
    pytest.main()

