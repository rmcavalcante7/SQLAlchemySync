import pytest
from models.revendedor import Revendedor


# @pytest.fixture
# def Revendedor():
#     return Revendedor(nome=nome)


nome = 'asdf'
cnpj = '12345678901234'
razao_social = 'teste ltda'
contato = '31 9999-6666'


@pytest.mark.order(8)
# Teste criação de instancias de Revendedor
def test_instancia_revendedor():
    revendedor = Revendedor(nome=nome, cnpj=cnpj, razao_social=razao_social, contato=contato)
    assert revendedor.nome == nome


# Teste de inserção bem-sucedida
def test_inserir_revendedor():
    revendedor = Revendedor.insertRevendedor(nome=nome, cnpj=cnpj, razao_social=razao_social, contato=contato)
    assert (revendedor.id is not None and
            revendedor.nome == nome.upper()
            )


# Teste de erro de integridade ao tentar inserir o mesmo registro duas vezes
def test_erro_integridade_mesma_combinacao():
    with pytest.raises(RuntimeError) as exc_info:
        Revendedor.insertRevendedor(nome=nome, cnpj=cnpj, razao_social=razao_social, contato=contato)
    assert f"Já existe um Revendedor com o CNPJ '{cnpj}' cadastrado." in str(exc_info.value)


# Teste de erro ao inserir tipos de dados incorretos
def test_tipo_dados_incorretos():
    with pytest.raises(TypeError) as exc_info1:
        Revendedor.insertRevendedor(nome=1234, cnpj=cnpj, razao_social=razao_social, contato=contato)

    assert 'nome do Revendedor deve ser uma string' in str(exc_info1.value)

    with pytest.raises(TypeError) as exc_info2:
        Revendedor.insertRevendedor(nome=nome, cnpj=1234, razao_social=razao_social, contato=contato)
    assert 'cnpj do Revendedor deve ser uma string' in str(exc_info2.value)

    with pytest.raises(TypeError) as exc_info3:
        Revendedor.insertRevendedor(nome=nome, cnpj=cnpj, razao_social=1234, contato=contato)
    assert 'razao_social do Revendedor deve ser uma string' in str(exc_info3.value)

    with pytest.raises(TypeError) as exc_info4:
        Revendedor.insertRevendedor(nome=nome, cnpj=cnpj, razao_social=razao_social, contato=1234)
    assert 'contato do Revendedor deve ser uma string' in str(exc_info4.value)


# Teste de erro ao inserir valores vazios
def test_valores_vazios():
    with pytest.raises(ValueError) as exc_info1:
        Revendedor.insertRevendedor(nome='', cnpj=cnpj, razao_social=razao_social, contato=contato)
    assert 'nome do Revendedor não informado!' in str(exc_info1.value)

    with pytest.raises(ValueError) as exc_info2:
        Revendedor.insertRevendedor(nome=nome, cnpj='', razao_social=razao_social, contato=contato)
    assert 'cnpj do Revendedor não informado!' in str(exc_info2.value)

    with pytest.raises(ValueError) as exc_info2:
        Revendedor.insertRevendedor(nome=nome, cnpj=cnpj[:10], razao_social=razao_social, contato=contato)
    assert 'cnpj do Revendedor deve ter 14 caracteres!' in str(exc_info2.value)

    with pytest.raises(ValueError) as exc_info3:
        Revendedor.insertRevendedor(nome=nome, cnpj=cnpj, razao_social='', contato=contato)
    assert 'razao_social do Revendedor não informada!' in str(exc_info3.value)

    with pytest.raises(ValueError) as exc_info4:
        Revendedor.insertRevendedor(nome=nome, cnpj=cnpj, razao_social=razao_social, contato='')
    assert 'contato do Revendedor não informado!' in str(exc_info4.value)


if __name__ == '__main__':
    pytest.main()
