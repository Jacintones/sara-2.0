"""
Constantes para validação de dados.
"""

# Padrões de Regex
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
TELEFONE_PATTERN = r'^\d{10,11}$'
CEP_PATTERN = r'^\d{8}$'

# Comprimentos
CNPJ_LENGTH = 14
CPF_LENGTH = 11
CEP_LENGTH = 8
RG_MIN_LENGTH = 5
RG_MAX_LENGTH = 14
NOME_MIN_WORDS = 2
SENHA_MIN_LENGTH = 8

# Formatos de Data
DATA_FORMAT_DEFAULT = '%Y-%m-%d'
DATA_FORMAT_BR = '%d/%m/%Y'
DATA_FORMAT_US = '%m/%d/%Y'

# Caracteres Especiais
SPECIAL_CHARS = '!@#$%^&*(),.?":{}|<>'

# Mensagens de Erro
ERRO_CNPJ_INVALIDO = "CNPJ inválido"
ERRO_CPF_INVALIDO = "CPF inválido"
ERRO_EMAIL_INVALIDO = "Email inválido"
ERRO_TELEFONE_INVALIDO = "Telefone inválido"
ERRO_DATA_INVALIDA = "Data inválida"
ERRO_CEP_INVALIDO = "CEP inválido"
ERRO_RG_INVALIDO = "RG inválido"
ERRO_NOME_INVALIDO = "Nome inválido"
ERRO_IE_INVALIDA = "Inscrição Estadual inválida"

# Mensagens de Erro de Senha
ERRO_SENHA_CURTA = "A senha deve ter no mínimo {} caracteres"
ERRO_SENHA_MAIUSCULA = "A senha deve conter pelo menos uma letra maiúscula"
ERRO_SENHA_MINUSCULA = "A senha deve conter pelo menos uma letra minúscula"
ERRO_SENHA_NUMERO = "A senha deve conter pelo menos um número"
ERRO_SENHA_ESPECIAL = "A senha deve conter pelo menos um caractere especial"

# Ranges Válidos
DDD_MIN = 11
DDD_MAX = 99

# Configurações de Validação
VALIDAR_NOME_COMPLETO = True  
VALIDAR_SENHA_FORTE = True    