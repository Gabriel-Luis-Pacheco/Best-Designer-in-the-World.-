# Product intelligence: safe proactivity

Proatividade útil é descobrir riscos e oportunidades, **não ampliar permissões**. A IA deve distinguir:
- **Dentro do objetivo e escopo:** melhorar problemas adjacentes, documentar causa, implementar e testar.
- **Fora do escopo:** explicar impacto e propor, sem alterar.
- **Contratos protegidos:** preços, pagamentos, dados fiscais, permissões, rotas críticas, marca; bloquear alterações silenciosas.
- **Mudança autorizada de alto risco:** ainda exige validação de domínio e regressão.

Usar `brain/decision_guard.py` com `brain/examples/scope-proposals.json` como modelo de contratos explícitos. A ferramenta é determinística, opera sobre IDs exatos e não substitui o diff nem gera permissão. Manter rastreabilidade entre proposta → contrato → teste → resultado.
