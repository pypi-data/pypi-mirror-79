

class Order:

    def __init__(self, code, sessionID,
                 email, totalValue, billing,
                 numberOfInstallments=1, ip=None, status=0,
                 **kwargs):
        self.__dict__.update(kwargs)
        self.code = code
        self.sessionID = sessionID
        self.email = email
        self.totalValue = totalValue
        self.numberOfInstallments = numberOfInstallments
        self.ip = ip
        self.status = status
        self.billing = billing
        self.payments = list()
        self.items = list()


class Billing:

    TYPE_PESSOA_FISICA = 1
    TYPE_PESSOA_JURIDICA = 2
    CUSTOMER_TYPES = (
        (TYPE_PESSOA_FISICA, u'Pessoa Física'),
        (TYPE_PESSOA_JURIDICA, u'Pessoa Jurídica'),
    )

    GENDER_MASCULINO = 'M'
    GENDER_FEMININO = 'F'
    GENDER_TYPES = (
        (GENDER_MASCULINO, u'Masculino'),
        (GENDER_FEMININO, u'Feminino'),
    )

    def __init__(self, customer_type, primaryDocument,
                 name, email, **kwargs):
        self.__dict__.update(kwargs)
        self.customer_type = customer_type
        self.primaryDocument = primaryDocument
        self.name = name
        self.email = email
        self.phones = list()


class Address:

    def __init__(self, street, number,
                 county, city, state,
                 zipcode, **kwargs):
        self.__dict__.update(kwargs)
        self.street = street
        self.number = number
        self.county = county
        self.city = city
        self.state = state
        self.zipcode = zipcode


class Phone:

    NAO_DEFINIDO = 0
    RESIDENCIAL = 1
    COMERCIAL = 2
    RECADOS = 3
    COBRANCA = 4
    TEMPORARIO = 5
    CELULAR = 6
    PHONE_TYPES = (
        (NAO_DEFINIDO, u'Não definido'),
        (RESIDENCIAL, u'Residencial'),
        (COMERCIAL, u'Comercial'),
        (RECADOS, u'Recados'),
        (COBRANCA, u'Cobrança'),
        (TEMPORARIO, u'Temporário'),
        (CELULAR, u'Celular'),
    )

    def __init__(self, phone_type, ddd, number, **kwargs):
        self.__dict__.update(kwargs)
        self.phone_type = phone_type
        self.ddd = ddd
        self.number = number


class Card:

    DINERS = 1
    MASTERCARD = 2
    VISA = 3
    OUTROS = 4
    AMERICAN_EXPRESS = 5
    HIPERCARD = 6
    AURA = 7
    ELO = 10
    LEADER_CARD = 50
    FORT_BRASIL = 100
    SOROCRED = 101
    A_VISTA = 102
    CARTAO_MAIS = 103
    CARTAO_CEA = 105
    CARD_TYPES = (
        (DINERS, u'Diners'),
        (MASTERCARD, u'MasterCard'),
        (VISA, u'Visa'),
        (OUTROS, u'Outros'),
        (AMERICAN_EXPRESS, u'American Express'),
        (HIPERCARD, u'HiperCard'),
        (AURA, u'Aura'),
        (ELO, u'Cartão Elo'),
        (LEADER_CARD, u'LeaderCard'),
        (FORT_BRASIL, u'Fortbrasil'),
        (SOROCRED, u'Sorocred'),
        (A_VISTA, u'A Vista'),
        (CARTAO_MAIS, u'Cartão Mais'),
        (CARTAO_CEA, u'Cartão C&A'),
    )

    def __init__(self, six_first_digits, four_last_digits,
                 validityDate, ownerName, document,
                 **kwargs):
        self.__dict__.update(kwargs)
        self.six_first_digits = six_first_digits
        self.four_last_digits = four_last_digits
        self.validityDate = validityDate
        self.ownerName = ownerName
        self.document = document

    @property
    def number(self):
        if self.six_first_digits and self.four_last_digits:
            return f'{self.six_first_digits}xxxxxx{self.four_last_digits}'
        return str()


class Payment:

    CARTAO_CREDITO = 1
    BOLETO_BANCARIO = 2
    DEBITO_BANCARIO = 3
    DEBITO_BANCARIO_DINHEIRO = 4
    DEBITO_BANCARIO_CHEQUE = 5
    TRANSFERENCIA_BANCARIA = 6
    SEDEX_A_COBRAR = 7
    CHEQUE = 8
    DINHEIRO = 9
    FINANCIAMENTO = 10
    FATURA = 11
    CUPOM = 12
    MULTICHEQUE = 13
    OUTROS = 14
    VALE = 16
    CARTAO_PRESENTE = 1041
    CARTAO_DEBITO = 4011
    PAYMENT_TYPES = (
        (CARTAO_CREDITO, u'Cartão de Crédito'),
        (BOLETO_BANCARIO, u'Boleto Bancário'),
        (DEBITO_BANCARIO, u'Débito Bancário'),
        (DEBITO_BANCARIO_DINHEIRO, u'Débito Bancário - Dinheiro'),
        (DEBITO_BANCARIO_CHEQUE, u'Débito Bancário - Cheque'),
        (TRANSFERENCIA_BANCARIA, u'Transferência Bancária'),
        (SEDEX_A_COBRAR, u'Sedex a cobrar'),
        (CHEQUE, u'Cheque'),
        (DINHEIRO, u'Dinheiro'),
        (FINANCIAMENTO, u'Financiamento'),
        (FATURA, u'Fatura'),
        (CUPOM, u'Cupom'),
        (MULTICHEQUE, u'Multicheque'),
        (OUTROS, u'Outros'),
        (VALE, u'Vale'),
        (CARTAO_PRESENTE, u'Cartão Presente Virual'),
        (CARTAO_DEBITO, u'Cartão de Débito / Transferência Eletrônica (CD)'),
    )

    def __init__(self, payment_type, card, installments=1, **kwargs):
        self.__dict__.update(kwargs)
        self.payment_type = payment_type
        self.card = card
        self.installments = installments


class Item:

    def __init__(self, code, name,
                 value, amount, sellerName,
                 sellerDocument, isMarketPlace=False, **kwargs):
        self.__dict__.update(kwargs)
        self.code = code
        self.name = name
        self.value = value
        self.amount = amount
        self.sellerName = sellerName
        self.sellerDocument = sellerDocument
        self.isMarketPlace = isMarketPlace
