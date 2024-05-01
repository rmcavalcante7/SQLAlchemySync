import pytest
from models.aditivo_nutritivo import AditivoNutritivo


# @pytest.fixture
# def AditivoNutritivo():
#     return AditivoNutritivo(nome='VITAMIna D', formula_quimica='C27H44O')


# Teste criação de instancias de AditivoNutritivo
@pytest.mark.order(2)
def test_instancia_aditivo_nutritivo():
    aditivo_nutritivo = AditivoNutritivo(nome='VITAMIna D', formula_quimica='C27H44O')
    assert aditivo_nutritivo.nome == 'VITAMIna D' and aditivo_nutritivo.formula_quimica == 'C27H44O'

    aditivo_nutritivo = AditivoNutritivo(nome='VITAMIna E', formula_quimica='C29H50O2')
    assert aditivo_nutritivo.nome == 'VITAMIna E' and aditivo_nutritivo.formula_quimica == 'C29H50O2'


# Teste de inserção bem-sucedida
def test_inserir_aditivo_nutritivo():
    aditivo_nutritivo = AditivoNutritivo.insertAditivoNutritivo(nome='VITAMIna D', formula_quimica='C27H44O')
    assert (aditivo_nutritivo.id is not None and
            aditivo_nutritivo.nome == 'VITAMIna D'.upper() and
            aditivo_nutritivo.formula_quimica == 'C27H44O'.upper())

    aditivo_nutritivo = AditivoNutritivo.insertAditivoNutritivo(nome='VITAMIna E', formula_quimica='C29H50O2')
    assert (aditivo_nutritivo.id is not None and
            aditivo_nutritivo.nome == 'VITAMIna E'.upper() and
            aditivo_nutritivo.formula_quimica == 'C29H50O2'.upper())


# Teste de erro de integridade ao tentar inserir o mesmo registro duas vezes
def test_erro_integridade_mesma_combinacao():
    nome = 'VITAMIna D'
    formula_quimica = 'dsajfaljf4517194781324290840faskdfkahf982389374918'  # formula quimica invalida
    with pytest.raises(RuntimeError) as exc_info:
        AditivoNutritivo.insertAditivoNutritivo(nome=nome, formula_quimica=formula_quimica)
    assert f"Já existe um AditivoNutritivo com o nome '{nome.upper()}' cadastrado" in str(exc_info.value)

    # nome aleatorio
    nome = 'dsajfaljf4517194781324290840faskdfkahf982389374918'
    formula_quimica = 'C27H44O'
    with pytest.raises(RuntimeError) as exc_info:
        AditivoNutritivo.insertAditivoNutritivo(nome=nome, formula_quimica=formula_quimica)
    assert f"Já existe um AditivoNutritivo com a fórmula química '{formula_quimica.upper()}' cadastrada" in str(exc_info.value)


# Teste de erro ao inserir tipos de dados incorretos
def test_tipo_dados_incorretos():
    with pytest.raises(TypeError) as exc_info1:
        AditivoNutritivo.insertAditivoNutritivo(nome=1, formula_quimica='C27H44O')

    with pytest.raises(TypeError) as exc_info2:
        AditivoNutritivo.insertAditivoNutritivo(nome='VITAMIna D', formula_quimica=1)

    assert 'nome do AditivoNutritivo deve ser uma string' in str(exc_info1.value)
    assert 'formula_quimica do AditivoNutritivo deve ser uma string' in str(exc_info2.value)


# Teste de erro ao inserir valores vazios
def test_valores_vazios():
    with pytest.raises(ValueError) as exc_info1:
        AditivoNutritivo.insertAditivoNutritivo(nome='', formula_quimica='C27H44O')

    with pytest.raises(ValueError) as exc_info2:
        AditivoNutritivo.insertAditivoNutritivo(nome='VITAMIna D', formula_quimica='')

    assert 'nome do AditivoNutritivo não informado!' in str(exc_info1.value)
    assert 'formula_quimica do AditivoNutritivo não informada!' in str(exc_info2.value)


if __name__ == '__main__':
    pytest.main()
