STATUS_NOVO = '0'
STATUS_APROVADO = '9'
STATUS_CANCELADO = '41'
STATUS_REPROVADO = '45'

REQUEST_STATUS_LABEL = {
    STATUS_NOVO: u"Novo (será analisado pelo ClearSale)",
    STATUS_APROVADO: u"Aprovado (irá ao ClearSale já aprovado e não será analisado)",
    STATUS_CANCELADO: u"Cancelado pelo cliente (irá ao ClearSale já cancelado e não será analisado)",
    STATUS_REPROVADO: u"Reprovado (irá ao ClearSale já reprovado e não será analisado)",
}
