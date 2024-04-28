import pytest
from models.nota_fiscal import NotaFiscal, insertNotaFiscal


# @pytest.fixture
# def NotaFiscal():
#     return NotaFiscal(valor=valor)


valor = 45.23
numero_serie = '123asdf456asdf2789123asd4012123434asdf123'
descricao = 'nota com os produtos vendidos para o nota_fiscal'
revendedor_fk = 1


@pytest.mark.order(10)
# Teste criação de instancias de NotaFiscal
def test_instancia_nota_fiscal():
    nota_fiscal = NotaFiscal(valor=valor, numero_serie=numero_serie, descricao=descricao, revendedor_fk=revendedor_fk)
    assert (nota_fiscal.valor == valor and
            nota_fiscal.numero_serie == numero_serie and
            nota_fiscal.descricao == descricao and
            nota_fiscal.revendedor_fk == revendedor_fk)


# Teste de inserção bem-sucedida
def test_inserir_nota_fiscal():
    nota_fiscal = insertNotaFiscal(valor=valor, numero_serie=numero_serie, descricao=descricao, revendedor_fk=revendedor_fk)
    assert (nota_fiscal.id is not None and
            nota_fiscal.valor == valor and
            nota_fiscal.numero_serie == numero_serie.upper() and
            nota_fiscal.descricao == descricao.strip().upper() and
            nota_fiscal.revendedor_fk == revendedor_fk
            )


# Teste de erro de integridade ao tentar inserir o mesmo registro duas vezes
def test_erro_integridade_mesma_combinacao():
    with pytest.raises(RuntimeError) as exc_info:
        insertNotaFiscal(valor=valor, numero_serie=numero_serie, descricao=descricao, revendedor_fk=revendedor_fk)
    assert f"Já existe uma Nota Fiscal com o número de série '{numero_serie.upper()}' cadastrado" in str(exc_info.value)


# Teste de erro ao inserir tipos de dados incorretos
def test_tipo_dados_incorretos():
    with pytest.raises(TypeError) as exc_info1:
        insertNotaFiscal(valor='1', numero_serie=numero_serie, descricao=descricao, revendedor_fk=revendedor_fk)
    assert 'valor da NotaFiscal deve ser um número!' in str(exc_info1.value)

    with pytest.raises(TypeError) as exc_info2:
        insertNotaFiscal(valor=valor, numero_serie=1, descricao=descricao, revendedor_fk=revendedor_fk)
    assert 'numero_serie da NotaFiscal deve ser uma string!' in str(exc_info2.value)

    with pytest.raises(TypeError) as exc_info3:
        insertNotaFiscal(valor=valor, numero_serie=numero_serie, descricao=1, revendedor_fk=revendedor_fk)
    assert 'descricao da NotaFiscal deve ser uma string!' in str(exc_info3.value)

    with pytest.raises(TypeError) as exc_info4:
        insertNotaFiscal(valor=valor, numero_serie=numero_serie, descricao=descricao, revendedor_fk='1')
    assert 'revendedor_fk da NotaFiscal deve ser um inteiro!' in str(exc_info4.value)


# Teste de erro ao inserir valores vazios
def test_valores_vazios():
    with pytest.raises(ValueError) as exc_info2:
        insertNotaFiscal(valor=valor, numero_serie='', descricao=descricao, revendedor_fk=revendedor_fk)
    assert 'numero_serie da NotaFiscal não informado!' in str(exc_info2.value)

    with pytest.raises(ValueError) as exc_info3:
        insertNotaFiscal(valor=valor, numero_serie=numero_serie, descricao='', revendedor_fk=revendedor_fk)
    assert 'descricao da NotaFiscal não informada!' in str(exc_info3.value)


# Test de erro ao inserir FK que não existe
def test_fk_nao_existe():
    numero_serie_novo = numero_serie + '1234'
    revendedor_fk_fake = 100
    with pytest.raises(RuntimeError) as exc_info:
        insertNotaFiscal(valor=valor, numero_serie=numero_serie_novo, descricao=descricao, revendedor_fk=revendedor_fk_fake)
    assert f"Verifique se a FK fornecida existe: {revendedor_fk=}" in str(exc_info.value)


if __name__ == '__main__':
    pytest.main()
