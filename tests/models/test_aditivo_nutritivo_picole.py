import pytest
from models.aditivo_nutritivo_picole import AditivoNutritivoPicole

picole_fk = 1
aditivo_nutritivo_fk = 1


@pytest.mark.order(11)
# Teste instanciando um objeto AditivoNutritivoPicole
def test_instanciar_aditivo_nutritivo():
    aditivo_nutritivo = AditivoNutritivoPicole(picole_fk=picole_fk, aditivo_nutritivo_fk=aditivo_nutritivo_fk)
    assert (isinstance(aditivo_nutritivo, AditivoNutritivoPicole) and
            aditivo_nutritivo.picole_fk == picole_fk and
            aditivo_nutritivo.aditivo_nutritivo_fk == aditivo_nutritivo_fk)


# Teste de inserção bem-sucedida
def test_inserir_aditivo_nutritivo():
    aditivo_nutritivo = AditivoNutritivoPicole.insertAditivoNutritivoPicole(picole_fk=picole_fk,
                                                                            aditivo_nutritivo_fk=aditivo_nutritivo_fk)
    assert aditivo_nutritivo.picole_fk == picole_fk and aditivo_nutritivo.aditivo_nutritivo_fk == aditivo_nutritivo_fk


# Teste de erro de integridade ao tentar inserir o mesmo registro duas vezes
def test_erro_integridade_mesma_combinacao():
    with pytest.raises(RuntimeError) as exc_info:
        AditivoNutritivoPicole.insertAditivoNutritivoPicole(picole_fk=picole_fk,
                                                            aditivo_nutritivo_fk=aditivo_nutritivo_fk)
    assert (f'Já existe um AditivoNutritivoPicole com a mesma combinação de picolé e aditivo nutritivo: '
            f'{picole_fk=} | {aditivo_nutritivo_fk=}') in str(exc_info.value)


# Teste de erro de integridade ao fornecer chaves estrangeiras inexistentes
def test_erro_integridade_chaves_estrangeiras():
    picole_fk_fake = 999
    aditivo_nutritivo_fk_fake = 999
    with pytest.raises(RuntimeError) as exc_info:
        AditivoNutritivoPicole.insertAditivoNutritivoPicole(picole_fk=picole_fk_fake,
                                                            aditivo_nutritivo_fk=aditivo_nutritivo_fk_fake)
    assert 'Erro de integridade ao inserir AditivoNutritivoPicole. Verifique se as FKs fornecidas existem' in str(
        exc_info.value)


# Teste de erro ao inserir tipos de dados incorretos
def test_tipo_dados_incorretos():
    with pytest.raises(TypeError) as exc_info1:
        AditivoNutritivoPicole.insertAditivoNutritivoPicole(picole_fk='abc',
                                                            aditivo_nutritivo_fk=aditivo_nutritivo_fk)

    with pytest.raises(TypeError) as exc_info2:
        AditivoNutritivoPicole.insertAditivoNutritivoPicole(picole_fk=picole_fk,
                                                            aditivo_nutritivo_fk='asdf')

    assert 'picole_fk do AditivoNutritivoPicole deve ser um inteiro!' in str(exc_info1.value)
    assert 'aditivo_nutritivo_fk do AditivoNutritivoPicole deve ser um inteiro!' in str(exc_info2.value)


# teste inserir combinação de picole_fk e aditivo_nutritivo_fk que já existe
def test_inserir_aditivo_nutritivo_combinacao_existente():
    with pytest.raises(RuntimeError) as exc_info:
        AditivoNutritivoPicole.insertAditivoNutritivoPicole(picole_fk=1,
                                                            aditivo_nutritivo_fk=1)
    assert (f"Já existe um AditivoNutritivoPicole com a mesma combinação de picolé e aditivo nutritivo: "
            f"{picole_fk=} | {aditivo_nutritivo_fk=}") in str(exc_info.value)


if __name__ == '__main__':
    pytest.main()
