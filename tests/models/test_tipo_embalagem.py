import pytest
from models.tipo_embalagem import TipoEmbalagem, insertTipoEmbalagem


# @pytest.fixture
# def TipoEmbalagem():
#     return TipoEmbalagem(nome=nome)


nome = 'Lacrado'

@pytest.mark.order(6)

# Teste criação de instancias de TipoEmbalagem
def test_instancia_tipo_embalagem():
    tipo_embalagem = TipoEmbalagem(nome=nome)
    assert tipo_embalagem.nome == nome


# Teste de inserção bem-sucedida
def test_inserir_tipo_embalagem():
    tipo_embalagem = insertTipoEmbalagem(nome=nome)
    assert (tipo_embalagem.id is not None and
            tipo_embalagem.nome == nome.upper()
            )


# Teste de erro de integridade ao tentar inserir o mesmo registro duas vezes
def test_erro_integridade_mesma_combinacao():
    with pytest.raises(RuntimeError) as exc_info:
        insertTipoEmbalagem(nome=nome)
    assert f"Já existe um TipoEmbalagem com o nome '{nome.upper()}' cadastrado" in str(exc_info.value)


# Teste de erro ao inserir tipos de dados incorretos
def test_tipo_dados_incorretos():
    with pytest.raises(TypeError) as exc_info1:
        insertTipoEmbalagem(nome=1)

    assert 'nome do TipoEmbalagem deve ser uma string' in str(exc_info1.value)


# Teste de erro ao inserir valores vazios
def test_valores_vazios():
    with pytest.raises(ValueError) as exc_info1:
        insertTipoEmbalagem(nome='')

    assert 'nome do TipoEmbalagem não informado!' in str(exc_info1.value)


if __name__ == '__main__':
    pytest.main()

