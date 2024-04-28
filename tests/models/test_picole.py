import pytest
from models.picole import Picole, insertPicole




# @pytest.fixture
# def insertPicole():
#     return insertPicole(tipo_picole_fk=tipo_picole_fk)


preco = 12.45
sabor_fk = 1
tipo_embalagem_fk = 1
tipo_picole_fk = 1
sabor_tipoPicole_tipoEmbalagem = f'{sabor_fk}_{tipo_picole_fk}_{tipo_embalagem_fk}'



@pytest.mark.order(9)
# Teste criação de instancia de Picole
def test_instancia_picole():
    picole = Picole(preco=preco, sabor_fk=sabor_fk, tipo_embalagem_fk=tipo_embalagem_fk,
                    tipo_picole_fk=tipo_picole_fk)
    assert (picole.preco == preco and
            picole.sabor_fk == sabor_fk and
            picole.tipo_embalagem_fk == tipo_embalagem_fk and
            picole.tipo_picole_fk == tipo_picole_fk
            )


# Teste de inserção bem-sucedida
def test_inserir_picole():
    picole = insertPicole(preco=preco, sabor_fk=sabor_fk, tipo_embalagem_fk=tipo_embalagem_fk,
                          tipo_picole_fk=tipo_picole_fk)
    assert (picole.id is not None and
            picole.preco == preco and
            picole.sabor_fk == sabor_fk and
            picole.tipo_embalagem_fk == tipo_embalagem_fk and
            picole.tipo_picole_fk == tipo_picole_fk
            )


# Teste de erro ao inserir tipos de dados incorretos
def test_tipo_dados_incorretos():
    with pytest.raises(TypeError) as exc_info1:
        insertPicole(preco='12.45', sabor_fk=sabor_fk, tipo_embalagem_fk=tipo_embalagem_fk,
                     tipo_picole_fk=tipo_picole_fk)
    assert 'preco do Picole deve ser numérico!' in str(exc_info1.value)

    with pytest.raises(TypeError) as exc_info2:
        insertPicole(preco=preco, sabor_fk='1', tipo_embalagem_fk=tipo_embalagem_fk,
                     tipo_picole_fk=tipo_picole_fk)
    assert 'sabor_fk do Picole deve ser um inteiro!' in str(exc_info2.value)

    with pytest.raises(TypeError) as exc_info3:
        insertPicole(preco=preco, sabor_fk=sabor_fk, tipo_embalagem_fk='1',
                     tipo_picole_fk=tipo_picole_fk)
    assert 'tipo_embalagem_fk do Picole deve ser um inteiro!' in str(exc_info3.value)

    with pytest.raises(TypeError) as exc_info4:
        insertPicole(preco=preco, sabor_fk=sabor_fk, tipo_embalagem_fk=tipo_embalagem_fk,
                     tipo_picole_fk='1')
    assert 'tipo_picole_fk do Picole deve ser um inteiro!' in str(exc_info4.value)


# Test de erro ao inserir FK que não existe
def test_fk_nao_existe():
    sabor_fk_fake = 999
    tipo_embalagem_fk_fake = 999
    tipo_picole_fk_fake = 999
    with pytest.raises(RuntimeError) as exc_info:
        insertPicole(preco=preco, sabor_fk=sabor_fk_fake, tipo_embalagem_fk=tipo_embalagem_fk,
                     tipo_picole_fk=tipo_picole_fk)
    assert (f"Verifique se as FKs fornecidas existem: sabor_fk={sabor_fk_fake} | tipo_embalagem_fk={tipo_embalagem_fk} | "
            f"tipo_picole_fk={tipo_picole_fk}"
            in str(exc_info.value))

    with pytest.raises(RuntimeError) as exc_info:
        insertPicole(preco=preco, sabor_fk=sabor_fk, tipo_embalagem_fk=tipo_embalagem_fk_fake,
                     tipo_picole_fk=tipo_picole_fk)
    assert (f"Verifique se as FKs fornecidas existem: sabor_fk={sabor_fk} | tipo_embalagem_fk={tipo_embalagem_fk_fake} | "
            f"tipo_picole_fk={tipo_picole_fk}"
            in str(exc_info.value))

    with pytest.raises(RuntimeError) as exc_info:
        insertPicole(preco=preco, sabor_fk=sabor_fk, tipo_embalagem_fk=tipo_embalagem_fk,
                     tipo_picole_fk=tipo_picole_fk_fake)
    assert (f"Verifique se as FKs fornecidas existem: sabor_fk={sabor_fk} | tipo_embalagem_fk={tipo_embalagem_fk} | "
            f"tipo_picole_fk={tipo_picole_fk_fake}"
             in str(exc_info.value))


# verificar se combinação já existe
def test_combinacao_ja_existe():
    with pytest.raises(RuntimeError) as exc_info:
        insertPicole(preco=preco, sabor_fk=sabor_fk, tipo_embalagem_fk=tipo_embalagem_fk,
                     tipo_picole_fk=tipo_picole_fk)
    assert (f"""Já existe um Picole com a mesma combinação de sabor_fk, tipo_picole_fk e tipo_embalagem_fk: {sabor_fk=} | {tipo_picole_fk=} | {tipo_embalagem_fk=}"""
            in str(exc_info.value))


if __name__ == '__main__':
    pytest.main()
