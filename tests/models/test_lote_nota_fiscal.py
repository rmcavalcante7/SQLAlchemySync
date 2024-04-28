import pytest
from models.lote_nota_fiscal import LoteNotaFiscal, insertLoteNotaFiscal


# @pytest.fixture
# def LoteNotaFiscal():
#     return LoteNotaFiscal(valor=valor)


nota_fiscal_fk = 1
lote_fk = 1


@pytest.mark.order(14)
# Teste criação de instancias de LoteNotaFiscal
def test_instancia_lote_nota_fiscal():
    lote_nota_fiscal = LoteNotaFiscal(nota_fiscal_fk=nota_fiscal_fk, lote_fk=lote_fk)
    assert (isinstance(lote_nota_fiscal, LoteNotaFiscal) and
            lote_nota_fiscal.nota_fiscal_fk == nota_fiscal_fk and
            lote_nota_fiscal.lote_fk == lote_fk)


# Teste de inserção bem-sucedida
def test_inserir_lote_nota_fiscal():
    lote_nota_fiscal = insertLoteNotaFiscal(nota_fiscal_fk=nota_fiscal_fk, lote_fk=lote_fk)
    assert (lote_nota_fiscal.id is not None and
            lote_nota_fiscal.nota_fiscal_fk == nota_fiscal_fk and
            lote_nota_fiscal.lote_fk == lote_fk
            )


# Teste de erro de integridade ao tentar inserir o mesmo registro duas vezes
def test_erro_integridade_mesma_combinacao():
    with pytest.raises(RuntimeError) as exc_info:
        insertLoteNotaFiscal(nota_fiscal_fk=nota_fiscal_fk, lote_fk=lote_fk)
    assert (f"Já existe um LoteNotaFiscal com a mesma combinação de lote e nota fiscal: "
            f"{nota_fiscal_fk=} | {lote_fk=}") in str(exc_info.value)


# Teste de erro ao inserir tipos de dados incorretos
def test_tipo_dados_incorretos():
    with pytest.raises(TypeError) as exc_info1:
        insertLoteNotaFiscal(nota_fiscal_fk='1', lote_fk=lote_fk)
    assert 'nota_fiscal_fk do LoteNotaFiscal deve ser um inteiro!' in str(exc_info1.value)

    with pytest.raises(TypeError) as exc_info2:
        insertLoteNotaFiscal(nota_fiscal_fk=nota_fiscal_fk, lote_fk='1')
    assert 'lote_fk do LoteNotaFiscal deve ser um inteiro!' in str(exc_info2.value)


# Test de erro ao inserir FK que não existe
def test_fk_nao_existe():
    nota_fiscal_fk = 9999
    lote_fk = 9999
    with pytest.raises(RuntimeError) as exc_info:
        insertLoteNotaFiscal(nota_fiscal_fk=nota_fiscal_fk, lote_fk=lote_fk)
    assert f"Verifique se as FKs fornecidas existem: {nota_fiscal_fk=} | {lote_fk=}" in str(exc_info.value)


if __name__ == '__main__':
    pytest.main()
