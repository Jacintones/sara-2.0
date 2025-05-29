
from django.db import models
from django.utils.translation import gettext_lazy as _

class Gender(models.TextChoices):
    MALE = 'M', _('Homem')
    FEMALE = 'F', _('Mulher')
    TRANSGENDER = 'T', _('Travesti')
    TRANSGENDER_WOMAN = 'W', _('Mulher Transexual')


class SexualOrientation(models.TextChoices):
    HETERO = 'M', _('Héterossexual')
    BI = 'F', _('Bissexual')
    HOMO = 'H', _('Homossexual')
    OTHER = 'O', _('Outro')


class Race(models.TextChoices):
    WHITE = 'W', _("Branco(a)")
    MULTIRACIAL = 'M', _("Pardo(a)")
    BLACK = 'B', _("Negro(a)")
    ASIAN = 'A', _("Amarelo(a)")
    INDIGENOUS = 'I', _("Indígena")


class CivilStatus(models.TextChoices):
    SINGLE = 'S',  _("Solteira")
    MARRIED = 'M',  _("Casada")
    WIDOWED = 'W',  _("Viúva")
    JUDICIALLY_SEPARATED = 'J',  _("Separada Judicialmente")
    DIVORCED = 'D',  _("Divorciada")
    COMMON_LAW_MARRIAGE = 'C',  _("União Estável")


class FederatedUnit(models.TextChoices):
    ACRE = 'AC', _('Acre')
    ALAGOAS = 'AL', _('Alagoas')
    AMAPA = 'AP', _('Amapá')
    AMAZONAS = 'AM', _('Amazonas')
    BAHIA = 'BA', _('Bahia')
    CEARA = 'CE', _('Ceará')
    DISTRITO_FEDERAL = 'DF', _('Distrito Federal')
    ESPIRITO_SANTO = 'ES', _('Espírito Santo')
    GOIAS = 'GO', _('Goiás')
    MARANHAO = 'MA', _('Maranhão')
    MATO_GROSSO = 'MT', _('Mato Grosso')
    MATO_GROSSO_DO_SUL = 'MS', _('Mato Grosso do Sul')
    MINAS_GERAIS = 'MG', _('Minas Gerais')
    PARA = 'PA', _('Pará')
    PARAIBA = 'PB', _('Paraíba')
    PARANA = 'PR', _('Paraná')
    PERNAMBUCO = 'PE', _('Pernambuco')
    PIAUI = 'PI', _('Piauí')
    RIO_DE_JANEIRO = 'RJ', _('Rio de Janeiro')
    RIO_GRANDE_DO_NORTE = 'RN', _('Rio Grande do Norte')
    RIO_GRANDE_DO_SUL = 'RS', _('Rio Grande do Sul')
    RONDONIA = 'RO', _('Rondônia')
    RORAIMA = 'RR', _('Roraima')
    SANTA_CATARINA = 'SC', _('Santa Catarina')
    SAO_PAULO = 'SP', _('São Paulo')
    SERGIPE = 'SE', _('Sergipe')
    TOCANTINS = 'TO', _('Tocantins')


class EducationLevel(models.TextChoices):
    NAO_ALFABETIZADA = 'NA', _('Não Alfabetizada')
    ENSINO_FUNDAMENTAL = 'EF', _('Ensino Fundamental')
    ENSINO_MEDIO = 'EM', _('Ensino Médio')
    CURSO_TECNOLOGO = 'CT', _('Curso Tecnólogo')
    ENSINO_SUPERIOR = 'ES', _('Ensino Superior')
    POS_GRADUACAO = 'PG', _('Pós Graduação')
    CURSO_TECNICO_PROF = 'CTP', _('Curso Técnico Profissionalizante')
    EJA_PROJOVEM = 'EJA', _('EJA / Projovem e Afins')


class Occupation(models.TextChoices):
    AUTONOMA = 'AUT', _('Autônoma')
    EMPREGADA = 'EMP', _('Empregada')
    DESEMPREGADA = 'DES', _('Desempregada')
    DO_LAR = 'DL', _('Do Lar')
    APOSENTADA_PENSIONISTA = 'AP', _('Aposentada/Pensionista')


class WorkStatus(models.TextChoices):
    TRABALHADORA_COM_CTPS = 'CTPS', _('Trabalhadora com CTPS')
    TRABALHADORA_SEM_CTPS = 'SCTPS', _('Trabalhadora sem CTPS')
    SERVIDORA_PUBLICA = 'SP', _('Servidora Pública')
    MILITAR = 'MIL', _('Militar')
    COM_PREVIDENCIA_SOCIAL = 'CPS', _('Com Previdência Social')
    SEM_PREVIDENCIA_SOCIAL = 'SPS', _('Sem Previdência Social')
    BENEFICIO_PRESTACAO_CONTINUADA = 'BPC', _('Benefício de Prestação Continuada')


class Income(models.TextChoices):
    MENOR_1_SM = 'M1SM', _('Menor de 1 SM')
    DE_1_A_3_SM = '1A3SM', _('de 1 a 3 SM')
    MAIS_DE_3_A_6_SM = '3A6SM', _('Mais de 3 a 6 SM')
    MAIS_DE_6_A_9_SM = '6A9SM', _('Mais de 6 a 9 SM')
    MAIS_DE_9_SM = '9SM', _('Mais de 9 SM')
    SEM_RENDA = 'SR', _('Sem Renda')


class Children(models.TextChoices):
    CHILD_1 = 'C1', _('1')
    CHILD_2 = 'C2', _('2')
    CHILD_3 = 'C3', _('3')
    CHILD_4 = 'C4', _('4')
    CHILD_5 = 'C5', _('5')
    CHILD_6 = 'C6', _('6')
    CHILD_7_OR_MORE = 'C7+', _('7 ou mais')


class Deficiency(models.TextChoices):
    PHYSICAL = 'PH', _('Física')
    AUDITORY = 'AU', _('Auditiva')
    VISUAL = 'VI', _('Visual')
    MENTAL = 'ME', _('Mental')
    OTHERS = 'OT', _('Outras')
    NONE = 'NO', _('Nenhuma')


class DrugUsage(models.TextChoices):
    MARIJUANA = 'MA', _('Maconha')
    COCAINE = 'CO', _('Cocaína')
    CRACK = 'CR', _('Crack')
    OTHERS = 'OT', _('Outras')
    NONE = 'NO', _('Nenhuma')


class AggressionSource(models.TextChoices):
    PANIC_BUTTON = 'PB', _('Botão de pânico')
    AUDIO_DETECTION = 'AD', _('Detecção por audio')