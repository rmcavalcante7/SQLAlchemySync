import pytest
from models.conservante import Conservante


# @pytest.fixture
# def Conservante():
#     return Conservante(nome=nome, descricao=descricao)


nome = 'Sorbato de Potássio1234d'
descricao = 'Utilizado para conservar alimentos. Evita a proliferação de fungos e leveduras.'


# Teste criação de instancias de Conservante
@pytest.mark.order(3)
def test_instancia_conservante():
    conservante = Conservante(nome=nome, descricao=descricao)
    assert conservante.nome == nome and conservante.descricao == descricao


# Teste de inserção bem-sucedida
def test_inserir_conservante():
    conservante = Conservante.insertConservante(nome=nome, descricao=descricao)
    assert (conservante.id is not None and
            conservante.nome == nome.upper() and
            conservante.descricao == descricao.upper())


# Teste de erro de integridade ao tentar inserir o mesmo registro duas vezes
def test_erro_integridade_mesma_combinacao():
    with pytest.raises(RuntimeError) as exc_info:
        Conservante.insertConservante(nome=nome, descricao=descricao)
    assert f"Já existe um Conservante com o nome '{nome.upper()}' cadastrado" in str(exc_info.value)


# Teste de erro ao inserir tipos de dados incorretos
def test_tipo_dados_incorretos():
    with pytest.raises(TypeError) as exc_info1:
        Conservante.insertConservante(nome=1, descricao=descricao)

    with pytest.raises(TypeError) as exc_info2:
        Conservante.insertConservante(nome=nome, descricao=1)

    assert 'nome do Conservante deve ser uma string' in str(exc_info1.value)
    assert 'descricao do Conservante deve ser uma string' in str(exc_info2.value)


# Teste de erro ao inserir valores vazios
def test_valores_vazios():
    with pytest.raises(ValueError) as exc_info1:
        Conservante.insertConservante(nome='', descricao=descricao)

    with pytest.raises(ValueError) as exc_info2:
        Conservante.insertConservante(nome=nome, descricao='')

    assert 'nome do Conservante não informado!' in str(exc_info1.value)
    assert 'descricao do Conservante não informada!' in str(exc_info2.value)


if __name__ == '__main__':
    pytest.main()
