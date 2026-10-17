# Lazarus — Apocalypse Reanimated Compat

Gerador de resource pack de compatibilidade para aplicar os modelos e animações do Reanimated Blue aos Walkers, Runners e Hordes do Apocalypse Now no Project Lazarus.

Este projeto é um **resource pack de compatibilidade**, acompanhado de um script Python para gerar o ZIP. Não é um mod Java/Forge independente.

Consulte o [guia completo de uso e aplicação](GUIA-DE-USO.md) para gerar, instalar, ativar, testar e integrar o patch à distribuição do modpack.

## Estado experimental

A estrutura JSON e a integridade do ZIP gerado foram verificadas. A seleção de variantes, as animações, as armaduras e a preservação de jogadores/NPCs ainda precisam de validação visual no Minecraft. Há um relato de textura preta/roxa em alguns zumbis naturais; a entidade e a causa ainda não foram identificadas, nem foi confirmada relação com este patch. Não tratar esta versão como estável.

## Ambiente usado

- Minecraft 1.20.1 / Forge.
- Apocalypse Now 3.0.5.
- Reanimated Blue v0.10.
- Entity Model Features 3.3.11 e Entity Texture Features 7.2.5.
- Tissou’s Zombie Pack 1.20.1 2.7 presente no modpack de teste.

O patch seleciona 33 Walkers, 24 Runners e 5 Hordes pelos IDs NBT. Os Crawlers estão fora do escopo, por decisão do projeto. As texturas próprias do Apocalypse Now são herdadas; o gerador não inclui PNGs.

## Gerar localmente

Python 3.9 ou superior, sem dependências adicionais:

```powershell
python scripts/build.py --instance "C:\caminho\da\instancia"
```

O script lê o JAR do Apocalypse Now e o ZIP do Reanimated em sua própria instalação, sem modificá-los. Caso existam várias versões, informe os arquivos explicitamente:

```powershell
python scripts/build.py --apocalypse "C:\packs\apocalypsenow-3.0.5-forge-1.20.1.jar" --reanimated "C:\packs\Reanimated.zip"
```

Saída: `dist/Lazarus - Apocalypse Reanimated Compat.zip`. Os modelos derivados e os arquivos originais não são versionados neste repositório. Cada colaborador gera o patch usando seus próprios arquivos.

## Instalar

1. Copie o ZIP gerado para `resourcepacks` da instância.
2. Ative-o na tela de resource packs, com prioridade acima do Reanimated e do Tissou.
3. Recarregue os recursos e confira o resultado em um mundo de teste.

O gerador não instala o patch nem altera `options.txt`. Para desfazer a instalação, desative o pack.

## Como funciona

Os renderizadores humanoides analisados do Apocalypse Now usam as camadas de modelo e armadura de jogador. O gerador adapta os arquivos `zombie.jem`, `zombie_inner_armor.jem` e `zombie_outer_armor.jem` do Reanimated para variantes das camadas `player`, `player_inner_armor` e `player_outer_armor`.

Arquivos `.properties` selecionam a variante 2 apenas para os IDs de Walker, Runner e Horde. As outras entidades selecionam a variante 1, correspondente ao modelo padrão. Esse comportamento é a intenção da implementação e ainda requer teste no jogo.

## Validação pendente

- Invocar `minecraft:zombie` repetidamente e verificar as variantes de textura.
- Conferir `apocalypsenow:walker_1` até `walker_33`.
- Conferir `apocalypsenow:runner_34` até `runner_57`.
- Conferir `apocalypsenow:horde_1` até `horde_5`.
- Conferir armaduras, itens nas mãos, jogador e NPCs.
- Comparar o mesmo zumbi com defeito com o patch ativo e desativado.

## Créditos e arquivos de terceiros

Os modelos e animações de origem pertencem ao autor do Reanimated Blue (mrblueyeti). Apocalypse Now, EMF, ETF e Tissou’s Zombie Pack pertencem aos respectivos autores. Este repositório contém o gerador e a documentação, sem incorporar os modelos de terceiros. A distribuição do ZIP gerado depende das permissões aplicáveis aos recursos de origem; nenhuma autorização de redistribuição foi verificada neste trabalho.
