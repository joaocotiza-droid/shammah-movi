# Shammah Moving — site

Landing page bilíngue (EN/PT) da Shammah Moving, Windermere/Orlando (FL).

## Como editar

Todo o texto (inglês e português), os serviços, os tipos de mudança e o FAQ ficam em `build.py`.

1. Edite os textos em `build.py`.
2. Rode `python3 build.py` para gerar o `index.html`.
3. Faça commit e push. A Vercel publica sozinha.

## Configurações rápidas (topo do `build.py`)

- `WA`: número do WhatsApp (só dígitos, com 1 na frente).
- `IG`: link do Instagram.
- `SITE_URL`: endereço público do site (usado nas prévias de link do WhatsApp e no Google). Troque quando ligar um domínio próprio.

## Link em português

`/?lang=pt` abre o site direto em português (bom para a bio do Instagram e para mandar no WhatsApp).

## Imagens

Ficam em `assets/`. Para trocar uma foto, mantenha o mesmo nome de arquivo.

## Pedido de mudança

O formulário de agendamento não usa banco de dados nem painel. Quando o cliente envia, o site monta um resumo (tipo de mudança, data desejada, janela de chegada, contato, endereços, tamanho, itens e observações) e abre o WhatsApp do número `WA` com a mensagem pronta. A resposta e o orçamento acontecem no próprio WhatsApp.
