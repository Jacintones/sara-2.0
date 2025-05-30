import re
from typing import Optional
from datetime import datetime
from utils.validation_patterns import (
    EMAIL_PATTERN, TELEFONE_PATTERN, CEP_PATTERN,
    CNPJ_LENGTH, CPF_LENGTH, CEP_LENGTH, RG_MIN_LENGTH, RG_MAX_LENGTH,
    NOME_MIN_WORDS, SENHA_MIN_LENGTH, DATA_FORMAT_DEFAULT,
    SPECIAL_CHARS, DDD_MIN, DDD_MAX, VALIDAR_SENHA_FORTE
)

def remove_mascara(valor: str) -> str:
    return re.sub(r'\D', '', valor) if valor else valor

class BusinessValidator:
    """Reusable business validators."""
    
    @staticmethod
    def validate_cnpj(cnpj: str) -> bool:
        cnpj = remove_mascara(cnpj)

        if len(cnpj) != CNPJ_LENGTH or not cnpj.isdigit():
            return False

        if len(set(cnpj)) == 1:
            return False

        total = 0
        weight = 5
        for i in range(12):
            total += int(cnpj[i]) * weight
            weight = weight - 1 if weight > 2 else 9

        digit1 = 11 - (total % 11)
        digit1 = 0 if digit1 > 9 else digit1

        if int(cnpj[12]) != digit1:
            return False

        total = 0
        weight = 6
        for i in range(13):
            total += int(cnpj[i]) * weight
            weight = weight - 1 if weight > 2 else 9

        digit2 = 11 - (total % 11)
        digit2 = 0 if digit2 > 9 else digit2

        return int(cnpj[13]) == digit2

    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        cpf = remove_mascara(cpf)

        if len(cpf) != CPF_LENGTH or not cpf.isdigit():
            return False

        if len(set(cpf)) == 1:
            return False

        total = 0
        for i in range(9):
            total += int(cpf[i]) * (10 - i)

        digit1 = 11 - (total % 11)
        digit1 = 0 if digit1 > 9 else digit1

        if int(cpf[9]) != digit1:
            return False

        total = 0
        for i in range(10):
            total += int(cpf[i]) * (11 - i)

        digit2 = 11 - (total % 11)
        digit2 = 0 if digit2 > 9 else digit2

        return int(cpf[10]) == digit2

    @staticmethod
    def validate_email(email: str) -> bool:
        return bool(re.match(EMAIL_PATTERN, email))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        phone = remove_mascara(phone)

        if not re.match(TELEFONE_PATTERN, phone):
            return False

        ddd = int(phone[:2])
        if ddd < DDD_MIN or ddd > DDD_MAX:
            return False

        if len(phone) == 11 and phone[2] != '9':
            return False

        return True

    @staticmethod
    def validate_date(date_str: str, format: str = DATA_FORMAT_DEFAULT) -> bool:
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_cep(cep: str) -> bool:
        cep = remove_mascara(cep)
        return bool(re.match(CEP_PATTERN, cep))

    @staticmethod
    def validate_rg(rg: str) -> bool:
        rg = remove_mascara(rg)
        return rg.isdigit() and RG_MIN_LENGTH <= len(rg) <= RG_MAX_LENGTH

    @staticmethod
    def validate_password(password: str, min_length: int = SENHA_MIN_LENGTH) -> tuple[bool, Optional[str]]:
        if len(password) < min_length:
            return False, f"A senha deve ter no mínimo {min_length} caracteres"

        if VALIDAR_SENHA_FORTE:
            if not re.search(r'[A-Z]', password):
                return False, "A senha deve conter pelo menos uma letra maiúscula"
            if not re.search(r'[a-z]', password):
                return False, "A senha deve conter pelo menos uma letra minúscula"
            if not re.search(r'\d', password):
                return False, "A senha deve conter pelo menos um número"
            if not any(c in SPECIAL_CHARS for c in password):
                return False, "A senha deve conter pelo menos um caractere especial"

        return True, None

    @staticmethod
    def validate_inscricao_estadual(ie: str, uf: str) -> bool:
        ie = remove_mascara(ie)
        return ie.isdigit() and 8 <= len(ie) <= 14
    
    @staticmethod
    def validate_schema_name(schema_name: str) -> bool:
        """
        Validates a schema_name according to PostgreSQL rules.
        
        Args:
            schema_name: schema name to validate

        Returns:
            bool: True if valid, False otherwise
        """
        if not schema_name:
            return False

        if len(schema_name) > 63:
            return False

        # Must start with a letter or underscore and contain only lowercase letters, digits, and underscores
        if not re.match(r"^[a-z_][a-z0-9_]*$", schema_name):
            return False

        return True


