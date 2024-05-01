import pytest
from models.ingrediente import Ingrediente


# @pytest.fixture
# def Ingrediente():
#     return Ingrediente(nome=nome)


nome = 'Cajamanga2'


@pytest.mark.order(4)
# Teste criação de instancias de Ingrediente
def test_instancia_ingrediente():
    ingrediente = Ingrediente(nome=nome)
    assert ingrediente.nome == nome


# Teste de inserção bem-sucedida
def test_inserir_ingrediente():
    ingrediente = Ingrediente.insertIngrediente(nome=nome)
    assert (ingrediente.id is not None and
            ingrediente.nome == nome.upper()
            )


# Teste de erro de integridade ao tentar inserir o mesmo registro duas vezes
def test_erro_integridade_mesma_combinacao():
    with pytest.raises(RuntimeError) as exc_info:
        Ingrediente.insertIngrediente(nome=nome)
    assert f"Já existe um Ingrediente com o nome '{nome.upper()}' cadastrado" in str(exc_info.value)


# Teste de erro ao inserir tipos de dados incorretos
def test_tipo_dados_incorretos():
    with pytest.raises(TypeError) as exc_info1:
        Ingrediente.insertIngrediente(nome=1)

    assert 'nome do Ingrediente deve ser uma string' in str(exc_info1.value)


# Teste de erro ao inserir valores vazios
def test_valores_vazios():
    with pytest.raises(ValueError) as exc_info1:
        Ingrediente.insertIngrediente(nome='')

    assert 'nome do Ingrediente não informado!' in str(exc_info1.value)


if __name__ == '__main__':
    pytest.main()

