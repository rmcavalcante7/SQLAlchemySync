import pytest
from models.lote import Lote, insertLote


# @pytest.fixture
# def insertLote():
#     return insertLote(picole_fk=picole_fk)


picole_fk = 1
quantidade = 20

@pytest.mark.order(10)
# Teste criação de instancias de insertLote
def test_instancia_lote():
    lote = Lote(picole_fk=picole_fk, quantidade=quantidade)
    assert (lote.picole_fk == picole_fk and
            lote.quantidade == quantidade)


# Teste de inserção bem-sucedida
def test_inserir_lote():
    lote = insertLote(picole_fk=picole_fk, quantidade=quantidade)
    assert (lote.id is not None and
            lote.picole_fk == picole_fk and
            lote.quantidade == quantidade
            )


# Teste de erro ao inserir tipos de dados incorretos
def test_tipo_dados_incorretos():
    with pytest.raises(TypeError) as exc_info1:
        insertLote(picole_fk='1', quantidade=quantidade)
    assert 'picole_fk deve ser um inteiro!' in str(exc_info1.value)

    with pytest.raises(TypeError) as exc_info2:
        insertLote(picole_fk=1.5, quantidade=quantidade)
    assert 'picole_fk deve ser um inteiro!' in str(exc_info2.value)

    with pytest.raises(TypeError) as exc_info3:
        insertLote(picole_fk=picole_fk, quantidade='20')
    assert 'quantidade deve ser um inteiro!' in str(exc_info3.value)

    with pytest.raises(TypeError) as exc_info4:
        insertLote(picole_fk=picole_fk, quantidade=20.5)
    assert 'quantidade deve ser um inteiro!' in str(exc_info4.value)


# Teste de erro ao inserir picole_fkes vazios
def test_picole_fkes_vazios():
    with pytest.raises(ValueError) as exc_info2:
        insertLote(picole_fk=picole_fk, quantidade=0)
    assert 'quantidade de picolés do Lote deve ser maior que zero!' in str(exc_info2.value)


# Test de erro ao inserir FK que não existe
def test_fk_nao_existe():
    picole_fk_fake = 100
    with pytest.raises(RuntimeError) as exc_info:
        insertLote(picole_fk=picole_fk_fake, quantidade=quantidade)
    assert f"Erro de integridade ao inserir Lote: {picole_fk=}" in str(exc_info.value)


if __name__ == '__main__':
    pytest.main()
