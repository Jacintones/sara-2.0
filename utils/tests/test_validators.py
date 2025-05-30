from django.test import TestCase
from utils.validators import BusinessValidator

class TestBusinessValidator(TestCase):
    def setUp(self):
        self.validator = BusinessValidator()

    def test_validar_cnpj(self):
        # CNPJs válidos
        self.assertTrue(self.validator.validar_cnpj('11.222.333/0001-81'))
        self.assertTrue(self.validator.validar_cnpj('11222333000181'))
        
        # CNPJs inválidos
        self.assertFalse(self.validator.validar_cnpj('11.222.333/0001-00'))
        self.assertFalse(self.validator.validar_cnpj('11111111111111'))
        self.assertFalse(self.validator.validar_cnpj('abc'))
        self.assertFalse(self.validator.validar_cnpj(''))

    def test_validar_cpf(self):
        # CPFs válidos
        self.assertTrue(self.validator.validar_cpf('529.982.247-25'))
        self.assertTrue(self.validator.validar_cpf('52998224725'))
        
        # CPFs inválidos
        self.assertFalse(self.validator.validar_cpf('111.111.111-11'))
        self.assertFalse(self.validator.validar_cpf('123.456.789-00'))
        self.assertFalse(self.validator.validar_cpf('abc'))
        self.assertFalse(self.validator.validar_cpf(''))

    def test_validar_email(self):
        # Emails válidos
        self.assertTrue(self.validator.validar_email('usuario@dominio.com'))
        self.assertTrue(self.validator.validar_email('usuario.nome@empresa.com.br'))
        self.assertTrue(self.validator.validar_email('usuario123@dominio.net'))
        
        # Emails inválidos
        self.assertFalse(self.validator.validar_email('usuario@'))
        self.assertFalse(self.validator.validar_email('@dominio.com'))
        self.assertFalse(self.validator.validar_email('usuario@dominio'))
        self.assertFalse(self.validator.validar_email('usuario.dominio.com'))

    def test_validar_telefone(self):
        # Telefones válidos
        self.assertTrue(self.validator.validar_telefone('(11) 99999-9999'))
        self.assertTrue(self.validator.validar_telefone('11999999999'))
        self.assertTrue(self.validator.validar_telefone('(11) 3333-3333'))
        self.assertTrue(self.validator.validar_telefone('1133333333'))
        
        # Telefones inválidos
        self.assertFalse(self.validator.validar_telefone('(00) 99999-9999'))
        self.assertFalse(self.validator.validar_telefone('(11) 8999-9999'))
        self.assertFalse(self.validator.validar_telefone('123'))
        self.assertFalse(self.validator.validar_telefone(''))

    def test_validar_data(self):
        # Datas válidas
        self.assertTrue(self.validator.validar_data('2023-12-31'))
        self.assertTrue(self.validator.validar_data('2024-02-29'))  # Ano bissexto
        
        # Datas inválidas
        self.assertFalse(self.validator.validar_data('2023-13-01'))
        self.assertFalse(self.validator.validar_data('2023-04-31'))
        self.assertFalse(self.validator.validar_data('abc'))
        
        # Formato diferente
        self.assertTrue(self.validator.validar_data('31/12/2023', '%d/%m/%Y'))
        self.assertFalse(self.validator.validar_data('31/12/2023', '%Y-%m-%d'))

    def test_validar_cep(self):
        # CEPs válidos
        self.assertTrue(self.validator.validar_cep('12345-678'))
        self.assertTrue(self.validator.validar_cep('12345678'))
        
        # CEPs inválidos
        self.assertFalse(self.validator.validar_cep('1234-567'))
        self.assertFalse(self.validator.validar_cep('abc'))
        self.assertFalse(self.validator.validar_cep(''))

    def test_validar_rg(self):
        # RGs válidos
        self.assertTrue(self.validator.validar_rg('12.345.678-9'))
        self.assertTrue(self.validator.validar_rg('123456789'))
        
        # RGs inválidos
        self.assertFalse(self.validator.validar_rg('1234'))
        self.assertFalse(self.validator.validar_rg('abc'))
        self.assertFalse(self.validator.validar_rg(''))

    def test_validar_senha(self):
        # Senhas válidas
        valido, msg = self.validator.validar_senha('Abc123@xyz')
        self.assertTrue(valido)
        self.assertIsNone(msg)
        
        # Senha muito curta
        valido, msg = self.validator.validar_senha('Abc@123')
        self.assertFalse(valido)
        self.assertIn('mínimo 8 caracteres', msg)
        
        # Sem letra maiúscula
        valido, msg = self.validator.validar_senha('abc123@xyz')
        self.assertFalse(valido)
        self.assertIn('letra maiúscula', msg)
        
        # Sem letra minúscula
        valido, msg = self.validator.validar_senha('ABC123@XYZ')
        self.assertFalse(valido)
        self.assertIn('letra minúscula', msg)
        
        # Sem número
        valido, msg = self.validator.validar_senha('AbcDef@xyz')
        self.assertFalse(valido)
        self.assertIn('número', msg)
        
        # Sem caractere especial
        valido, msg = self.validator.validar_senha('Abc123xyz')
        self.assertFalse(valido)
        self.assertIn('caractere especial', msg)

    def test_validar_inscricao_estadual(self):
        # IEs válidas
        self.assertTrue(self.validator.validar_inscricao_estadual('123456789', 'SP'))
        self.assertTrue(self.validator.validar_inscricao_estadual('12345678', 'RJ'))
        
        # IEs inválidas
        self.assertFalse(self.validator.validar_inscricao_estadual('1234567', 'SP'))  # Muito curta
        self.assertFalse(self.validator.validar_inscricao_estadual('123456789012345', 'SP'))  # Muito longa
        self.assertFalse(self.validator.validar_inscricao_estadual('abc', 'SP'))  # Não numérica
        self.assertFalse(self.validator.validar_inscricao_estadual('', 'SP')) 