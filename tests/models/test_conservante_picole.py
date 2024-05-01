import pytest
from models.conservante_picole import ConservantePicole

picole_fk = 1
conservante_fk = 1


@pytest.mark.order(12)
# Teste instanciando um objeto ConservantePicole
def test_instanciar_conservante_picole():
    conservante_picole = ConservantePicole(picole_fk=picole_fk, conservante_fk=conservante_fk)
    assert (isinstance(conservante_picole, ConservantePicole) and
            conservante_picole.picole_fk == picole_fk and
            conservante_picole.conservante_fk == conservante_fk)


# Teste de inserção bem-sucedida
def test_inserir_conservante_picole():
    conservante_picole = ConservantePicole.insertConservantePicole(picole_fk=picole_fk, conservante_fk=conservante_fk)
    assert conservante_picole.picole_fk == picole_fk and conservante_picole.conservante_fk == conservante_fk


# Teste de erro de integridade ao tentar inserir o mesmo registro duas vezes
def test_erro_integridade_mesma_combinacao():
    with pytest.raises(RuntimeError) as exc_info:
        ConservantePicole.insertConservantePicole(picole_fk=picole_fk, conservante_fk=conservante_fk)
    assert 'Já existe um ConservantePicole com a mesma combinação de picole_fk e conservante_fk' in str(exc_info.value)


# Teste de erro de integridade ao fornecer chaves estrangeiras inexistentes
def test_erro_integridade_chaves_estrangeiras():
    picole_fk_fake = 999
    conservante_fk_fake = 999
    with pytest.raises(RuntimeError) as exc_info:
        ConservantePicole.insertConservantePicole(picole_fk=picole_fk_fake, conservante_fk=conservante_fk_fake)
    assert 'Erro de integridade ao inserir ConservantePicole. Verifique se as FKs fornecidas existem' in str(
        exc_info.value)


# Teste de erro ao inserir tipos de dados incorretos
def test_tipo_dados_incorretos():
    with pytest.raises(TypeError) as exc_info1:
        ConservantePicole.insertConservantePicole(picole_fk='abc', conservante_fk=conservante_fk)

    with pytest.raises(TypeError) as exc_info2:
        ConservantePicole.insertConservantePicole(picole_fk=picole_fk, conservante_fk='asdf')

    assert 'picole_fk do ConservantePicole deve ser um inteiro!' in str(exc_info1.value)
    assert 'conservante_fk do ConservantePicole deve ser um inteiro!' in str(exc_info2.value)


# teste inserir combinação de picole_fk e conservante_fk que já existe
def test_inserir_conservante_picole_combinacao_existente():
    with pytest.raises(RuntimeError) as exc_info:
        ConservantePicole.insertConservantePicole(picole_fk=1, conservante_fk=1)
    assert (f"Já existe um ConservantePicole com a mesma combinação de picole_fk e conservante_fk: {picole_fk=} | "
            f"{conservante_fk=}") in str(exc_info.value)


if __name__ == '__main__':
    pytest.main()
