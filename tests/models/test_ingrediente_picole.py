import pytest
from models.ingrediente_picole import IngredientePicole, insertIngredientePicole

picole_fk = 1
ingrediente_fk = 1


@pytest.mark.order(13)
# Teste instanciando um objeto IngredientePicole
def test_instanciar_ingrediente_picole():
    ingrediente_picole = IngredientePicole(picole_fk=picole_fk, ingrediente_fk=ingrediente_fk)
    assert (isinstance(ingrediente_picole, IngredientePicole) and
            ingrediente_picole.picole_fk == picole_fk and
            ingrediente_picole.ingrediente_fk == ingrediente_fk)


# Teste de inserção bem-sucedida
def test_inserir_ingrediente_picole():
    ingrediente_picole = insertIngredientePicole(picole_fk=picole_fk, ingrediente_fk=ingrediente_fk)
    assert ingrediente_picole.picole_fk == picole_fk and ingrediente_picole.ingrediente_fk == ingrediente_fk


# Teste de erro de integridade ao tentar inserir o mesmo registro duas vezes
def test_erro_integridade_mesma_combinacao():
    with pytest.raises(RuntimeError) as exc_info:
        insertIngredientePicole(picole_fk=picole_fk, ingrediente_fk=ingrediente_fk)
    assert 'Já existe um IngredientePicole com a mesma combinação de picole_fk e ingrediente_fk' in str(exc_info.value)


# Teste de erro de integridade ao fornecer chaves estrangeiras inexistentes
def test_erro_integridade_chaves_estrangeiras():
    picole_fk_fake = 999
    ingrediente_fk_fake = 999
    with pytest.raises(RuntimeError) as exc_info:
        insertIngredientePicole(picole_fk=picole_fk_fake, ingrediente_fk=ingrediente_fk_fake)
    assert 'Erro de integridade ao inserir IngredientePicole. Verifique se as FKs fornecidas existem' in str(
        exc_info.value)


# Teste de erro ao inserir tipos de dados incorretos
def test_tipo_dados_incorretos():
    with pytest.raises(TypeError) as exc_info1:
        insertIngredientePicole(picole_fk='abc', ingrediente_fk=ingrediente_fk)

    with pytest.raises(TypeError) as exc_info2:
        insertIngredientePicole(picole_fk=picole_fk, ingrediente_fk='asdf')

    assert 'picole_fk do IngredientePicole deve ser um inteiro' in str(exc_info1.value)
    assert 'ingrediente_fk do IngredientePicole deve ser um inteiro' in str(exc_info2.value)


# teste inserir combinação de picole_fk e ingrediente_fk já existente
def test_inserir_ingrediente_picole_combinacao_existente():
    with pytest.raises(RuntimeError) as exc_info:
        insertIngredientePicole(picole_fk=picole_fk, ingrediente_fk=ingrediente_fk)
    assert f'Já existe um IngredientePicole com a mesma combinação de picole_fk e ingrediente_fk: {picole_fk=} | {ingrediente_fk=}' in str(
        exc_info.value)


if __name__ == '__main__':
    pytest.main()
