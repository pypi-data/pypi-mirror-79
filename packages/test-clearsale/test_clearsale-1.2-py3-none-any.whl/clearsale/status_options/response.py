# Approved
STATUS_SAIDA_APROVACAO_AUTOMATICA = 'APA'
STATUS_SAIDA_APROVACAO_MANUAL = 'APM'
STATUS_SAIDA_APROVACAO_POR_POLITICA = 'APP'

# In analysis
STATUS_SAIDA_NOVO = 'NVO'
STATUS_SAIDA_ANALISE_MANUAL = 'AMA'

# Not approved
STATUS_SAIDA_REPROVADA_SEM_SUSPEITA = 'RPM'
STATUS_SAIDA_SUSPENSAO_MANUAL = 'SUS'
STATUS_SAIDA_CANCELADO_PELO_CLIENTE = 'CAN'
STATUS_SAIDA_FRAUDE_CONFIRMADA = 'FRD'
STATUS_SAIDA_REPROVACAO_AUTOMATICA = 'RPA'
STATUS_SAIDA_REPROVACAO_POR_POLITICA = 'RPP'

# Error
STATUS_SAIDA_ERRO = 'ERR'

# Status lists
STATUS_APPROVED_LIST = (
    STATUS_SAIDA_APROVACAO_AUTOMATICA,
    STATUS_SAIDA_APROVACAO_MANUAL,
    STATUS_SAIDA_APROVACAO_POR_POLITICA,
)

STATUS_WAITING_FOR_APPROVAL_LIST = (
    STATUS_SAIDA_NOVO,
    STATUS_SAIDA_ANALISE_MANUAL,
)

STATUS_NOT_APPROVED_LIST = (
    STATUS_SAIDA_REPROVADA_SEM_SUSPEITA,
    STATUS_SAIDA_SUSPENSAO_MANUAL,
    STATUS_SAIDA_CANCELADO_PELO_CLIENTE,
    STATUS_SAIDA_FRAUDE_CONFIRMADA,
    STATUS_SAIDA_REPROVACAO_AUTOMATICA,
    STATUS_SAIDA_REPROVACAO_POR_POLITICA,
)

STATUS_ERROS_LIST = (
    STATUS_SAIDA_ERRO,
)

RESPONSE_STATUS_LABEL = {
    STATUS_SAIDA_APROVACAO_AUTOMATICA: u"(Aprovação Automática) – Pedido foi aprovado automaticamente segundo parâmetros definidos na regra de aprovação automática.",
    STATUS_SAIDA_APROVACAO_MANUAL: u"(Aprovação Manual) – Pedido aprovado manualmente por tomada de decisão de um analista.",
    STATUS_SAIDA_REPROVADA_SEM_SUSPEITA: u"(Reprovado Sem Suspeita) – Pedido Reprovado sem Suspeita por falta de contato com o cliente dentro do período acordado e/ou políticas restritivas de CPF (Irregular, SUS ou Cancelados)",
    STATUS_SAIDA_ANALISE_MANUAL: u"(Análise manual) – Pedido está em fila para análise",
    STATUS_SAIDA_ERRO: u"(Erro) - Ocorreu um erro na integração do pedido, sendo necessário analisar um possível erro no XML enviado e após a correção reenvia-lo.",
    STATUS_SAIDA_NOVO: u"(Novo) – Pedido importado e não classificado Score pela analisadora (processo que roda o Score de cada pedido).",
    STATUS_SAIDA_SUSPENSAO_MANUAL: u"(Suspensão Manual) – Pedido Suspenso por suspeita de fraude baseado no contato com o 'cliente' ou ainda na base ClearSale.",
    STATUS_SAIDA_CANCELADO_PELO_CLIENTE: u"(Cancelado pelo Cliente) – Cancelado por solicitação do cliente ou duplicidade do pedido.",
    STATUS_SAIDA_FRAUDE_CONFIRMADA: u"(Fraude Confirmada) – Pedido imputado como Fraude Confirmada por contato com a administradora de cartão e/ou contato com titular do cartão ou CPF do cadastro que desconhecem a compra.",
    STATUS_SAIDA_REPROVACAO_AUTOMATICA: u"(Reprovação Automática) – Pedido Reprovado Automaticamente por algum tipo de Regra de Negócio que necessite aplicá-la (Obs: não usual e não recomendado).",
    STATUS_SAIDA_REPROVACAO_POR_POLITICA: u"(Reprovação Por Política) – Pedido reprovado automaticamente por política estabelecida pelo cliente ou ClearSale.",
    STATUS_SAIDA_APROVACAO_POR_POLITICA: u"(Aprovação Por Política) – Pedido aprovado automaticamente por política estabelecida pelo cliente ou Clearsale.",
}
