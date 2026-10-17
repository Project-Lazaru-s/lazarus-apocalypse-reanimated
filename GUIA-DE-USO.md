# Lazarus — Guia de uso e aplicação do patch de animações

## 1. O que é este projeto

O **Lazarus — Apocalypse Reanimated Compat** é um resource pack de compatibilidade experimental. Seu objetivo é aplicar os modelos e animações de zumbi do **Reanimated Blue** aos Walkers, Runners e Hordes do **Apocalypse Now** no Project Lazarus.

Não é um mod Java e não gera um arquivo `.jar`. O resultado da geração é um arquivo `.zip`, instalado na pasta `resourcepacks` do Minecraft.

O repositório contém um gerador Python e documentação. Os modelos de terceiros são lidos dos arquivos que o desenvolvedor já possui localmente e incorporados ao ZIP gerado. Os arquivos originais não são modificados.

> **Estado experimental:** a estrutura JSON e a integridade do ZIP foram verificadas. O funcionamento visual completo ainda precisa ser validado no Minecraft. Há um relato de textura preta e roxa em alguns zumbis que surgiram naturalmente; a causa e a possível relação com este patch ainda não foram confirmadas.

## 2. Ambiente de referência

| Componente | Versão usada na preparação |
| --- | --- |
| Minecraft | 1.20.1 |
| Carregador | Forge |
| Apocalypse Now | 3.0.5 |
| Reanimated Blue | v0.10 |
| Entity Model Features — EMF | 3.3.11 |
| Entity Texture Features — ETF | 7.2.5 |
| Tissou’s Zombie Pack | 1.20.1 / 2.7 |

O EMF carrega os modelos e suas animações. O ETF participa da seleção das variantes por regras. O Tissou está presente no ambiente de teste para as texturas dos zumbis comuns; o gerador não extrai arquivos dele.

Não foi verificada compatibilidade com outras versões desses componentes.

## 3. Entidades abrangidas

| Família | IDs selecionados | Quantidade |
| --- | --- | ---: |
| Walker | `apocalypsenow:walker_1` até `apocalypsenow:walker_33` | 33 |
| Runner | `apocalypsenow:runner_34` até `apocalypsenow:runner_57` | 24 |
| Horde | `apocalypsenow:horde_1` até `apocalypsenow:horde_5` | 5 |
| **Total** | | **62** |

Os Crawlers estão fora do escopo por decisão do projeto. Sobreviventes, saqueadores, militares e jogadores não fazem parte da seleção pretendida. A preservação visual dessas entidades precisa ser conferida durante os testes.

## 4. Como o patch funciona

Os renderizadores humanoides analisados do Apocalypse Now utilizam camadas de modelo e armadura de jogador. Por isso, colocar apenas um modelo de zumbi comum no resource pack não faz essas entidades utilizarem automaticamente as mesmas animações.

O gerador lê três arquivos do Reanimated Blue:

```text
assets/minecraft/optifine/cem/zombie.jem
assets/minecraft/optifine/cem/zombie_inner_armor.jem
assets/minecraft/optifine/cem/zombie_outer_armor.jem
```

E os utiliza como variantes destas camadas:

```text
assets/minecraft/optifine/cem/player2.jem
assets/minecraft/optifine/cem/player_inner_armor2.jem
assets/minecraft/optifine/cem/player_outer_armor2.jem
```

Arquivos `.properties` selecionam a variante 2 quando o campo NBT `id` corresponde a um dos 62 IDs previstos. Para as outras entidades, as regras selecionam a variante 1, correspondente ao modelo padrão. Esse comportamento é a intenção da implementação e ainda requer validação dentro do jogo.

O ZIP não contém imagens PNG nem define uma textura própria de zumbi. A intenção é herdar a textura fornecida pelo renderizador da entidade, preservando a aparência do Apocalypse Now.

## 5. Para o desenvolvedor: gerar o ZIP

### Requisitos

- Python 3.9 ou superior.
- Acesso ao JAR do Apocalypse Now 3.0.5 e ao ZIP do Reanimated Blue v0.10.
- Uma cópia deste repositório no computador.

O script utiliza apenas a biblioteca padrão do Python. Não é necessário instalar pacotes com `pip`.

### Opção A — usar a pasta da instância

Abra o terminal na raiz deste repositório e execute:

```powershell
python scripts/build.py --instance "C:\caminho\da\instancia"
```

Se no Windows o Python estiver disponível pelo inicializador `py`, use:

```powershell
py -3 scripts/build.py --instance "C:\caminho\da\instancia"
```

O caminho da instância é a pasta que contém `mods`, `resourcepacks`, `config` e `options.txt`. No CurseForge, abra o perfil do modpack e use a opção **Abrir pasta**.

O script procura um JAR `apocalypsenow-*.jar` em `mods` e um ZIP `*Reanimated*.zip` em `resourcepacks`, ignorando o próprio patch com seu nome padrão. Se encontrar várias versões de origem, será necessário informar os arquivos explicitamente.

### Opção B — informar os arquivos de origem

```powershell
python scripts/build.py --apocalypse "C:\arquivos\apocalypsenow-3.0.5-forge-1.20.1.jar" --reanimated "C:\arquivos\Reanimated.zip"
```

Os caminhos e nomes são exemplos. Use os arquivos reais da instalação, incluindo quaisquer espaços ou caracteres especiais no nome.

### Escolher outro destino

```powershell
python scripts/build.py --instance "C:\caminho\da\instancia" --output "dist\Lazarus - Apocalypse Reanimated Compat.zip"
```

O script substitui o arquivo de saída se ele já existir. Para preservar uma geração anterior, escolha outro nome ou guarde uma cópia antes.

### Resultado esperado

Por padrão, o arquivo gerado fica em:

```text
dist/Lazarus - Apocalypse Reanimated Compat.zip
```

Ao terminar, o terminal informa o caminho, a quantidade de IDs e o SHA-256 do ZIP. O gerador verifica os IDs esperados, a leitura dos modelos, a integridade do ZIP e a sintaxe JSON. Essas verificações não equivalem a um teste visual das animações.

O gerador não instala o ZIP, não habilita resource packs e não altera `options.txt`.

## 6. Para o jogador: instalar e ativar

Se o responsável pelo Lazarus fornecer o ZIP pronto, o jogador não precisa instalar Python nem executar o gerador.

1. Feche o jogo antes de organizar os arquivos da instância.
2. No CurseForge, abra o perfil correto do Lazarus e selecione **Abrir pasta**.
3. Coloque o ZIP do patch dentro de `resourcepacks`, sem extraí-lo.
4. Inicie o Minecraft pelo perfil do Lazarus.
5. Abra **Opções → Pacotes de recursos**.
6. Ative **Lazarus - Apocalypse Reanimated Compat**.
7. Posicione o patch acima do Reanimated Blue e do Tissou’s Zombie Pack na lista de packs selecionados. Os packs mais acima têm prioridade.
8. Clique em **Concluído** e aguarde o recarregamento.
9. Entre em um mundo de teste e confira as entidades.

Estrutura esperada:

```text
instancia-do-lazarus/
  mods/
    apocalypsenow-3.0.5-forge-1.20.1.jar
    entity_model_features-3.3.11-1.20.1-forge.jar
    entity_texture_features-7.2.5-1.20.1-forge.jar
  resourcepacks/
    [arquivo do Reanimated Blue].zip
    TZP_1.20.1_2.7.zip
    Lazarus - Apocalypse Reanimated Compat.zip
```

O patch aparece no menu de **Pacotes de recursos** do Minecraft. Ele não aparece como mod na lista de arquivos `.jar` do CurseForge.

## 7. Para a equipe: integrar à distribuição do Lazarus

O GitHub guarda o gerador e as instruções de desenvolvimento. Apenas clonar o repositório não instala nem ativa o patch na instância de um jogador.

O fluxo de integração previsto é:

1. Usar as versões de origem documentadas.
2. Gerar o ZIP localmente.
3. Validar o patch no jogo.
4. Confirmar as permissões de distribuição dos recursos derivados.
5. Incluir o ZIP na pasta `resourcepacks` entregue pelo modpack, se a distribuição estiver autorizada.
6. Aplicar a ativação padrão pelo mecanismo de configuração que a equipe adotar, ou documentar a ativação manual para o jogador.
7. Importar a distribuição em uma instância nova e conferir se o ZIP chegou e se está ativo.

Em um pacote que utilize a estrutura de overrides do CurseForge, o destino esperado do arquivo é:

```text
overrides/resourcepacks/Lazarus - Apocalypse Reanimated Compat.zip
```

A ativação não é garantida pela simples presença do ZIP. O script deste repositório não implementa exportação do CurseForge nem gerenciamento de configurações padrão.

Não copie o `options.txt` pessoal inteiro de um desenvolvedor sem revisar seu conteúdo: ele também guarda outras preferências do jogo. Registre a ativação pelo fluxo de distribuição escolhido pela equipe.

## 8. Roteiro de teste no jogo

Use um mundo de teste com comandos habilitados, uma área coberta e espaço para observar os mobs sem interferência do sol.

### Zumbi comum do Minecraft

```mcfunction
/summon minecraft:zombie ~ ~ ~ {PersistenceRequired:1b}
```

Invoque vários para observar as diferentes texturas selecionadas pelo Tissou/ETF. Esses zumbis não fazem parte da seleção de IDs do patch, mas devem ser testados para detectar interações indesejadas.

### Apocalypse Now

```mcfunction
/summon apocalypsenow:walker_1 ~ ~ ~ {PersistenceRequired:1b}
/summon apocalypsenow:runner_34 ~ ~ ~ {PersistenceRequired:1b}
/summon apocalypsenow:horde_1 ~ ~ ~ {PersistenceRequired:1b}
```

Repita variando os números conforme a tabela de cobertura. Confira movimento, posição dos braços, cabeça e pernas, armaduras e itens nas mãos.

### Usar um botão no command block

Configure o bloco como **Impulso / Incondicional / Precisa de redstone**. Coloque um botão na lateral e escreva o comando dentro do bloco, sem a barra inicial:

```mcfunction
summon apocalypsenow:walker_1 ~ ~2 ~ {PersistenceRequired:1b}
```

Cada clique no botão invoca uma entidade, dois blocos acima do command block. Para testar outro ID, edite o comando. Esse exemplo não alterna IDs automaticamente.

### Verificações adicionais

- Observar o jogador em terceira pessoa.
- Conferir os NPCs humanos do Apocalypse Now.
- Conferir zumbis com armadura e com itens nas mãos.
- Confirmar que os Crawlers continuam com o comportamento visual anterior.
- Comparar as mesmas entidades com o patch ativo e desativado.

## 9. Solução de problemas

### O patch não aparece no menu

Confirme que o arquivo está na pasta `resourcepacks` da instância que foi iniciada. Abra o ZIP e confira se `pack.mcmeta` está na raiz, junto de `assets`, sem uma pasta extra envolvendo esses arquivos.

Se você baixou o código-fonte pelo botão **Download ZIP** do GitHub, esse arquivo é uma cópia do repositório, não o resource pack gerado. Execute o gerador ou obtenha um ZIP de patch fornecido pela equipe.

### Os zumbis continuam sem animação

Confira as versões do Minecraft, Forge, EMF e ETF; confirme que o patch e o Reanimated estão selecionados e que o patch está acima dos demais. Verifique também se o mob pertence a uma das famílias abrangidas. Crawlers não são atendidos.

Consulte `logs/latest.log` da instância em busca de mensagens do EMF e ETF. Uma geração concluída sem erro não confirma que o jogo selecionou e animou o modelo esperado.

### Alguns zumbis ficam pretos e roxos

Há um relato desse sintoma em alguns zumbis naturais. A verificação local conseguiu abrir 3.553 PNGs de zumbis na pasta correspondente do Tissou sem erro de decodificação. Isso não confirma que o jogo encontra ou seleciona corretamente cada textura em execução.

Para investigar:

1. Observe um zumbi que já apresenta a falha.
2. Desative apenas o patch de compatibilidade.
3. Aguarde o recarregamento e observe o mesmo zumbi novamente.
4. Registre se o defeito desapareceu ou permaneceu.
5. Identifique o ID da entidade, se possível, e preserve o trecho relevante de `logs/latest.log`.

Se a falha desaparecer, isso é evidência de uma interação com o patch. Se permanecer, será necessário investigar os outros recursos e renderizadores envolvidos. Não atribua a causa ao Tissou ou a outro componente apenas pela aparência.

### Armaduras ou jogador ficam deformados

Desative o patch e compare o resultado. Como a implementação utiliza variantes das camadas de jogador, esse é um ponto importante de validação. Registre o ID do mob, o equipamento utilizado, as versões e uma imagem do resultado.

### O gerador encontra vários arquivos de origem

Use `--apocalypse` e `--reanimated` para escolher explicitamente os arquivos corretos. O gerador não escolhe automaticamente entre várias versões.

### O gerador informa IDs diferentes do esperado

O código exige a seleção conhecida de 62 IDs da versão de referência. Se outra versão do Apocalypse Now alterar essa lista, revise o código e os modelos antes de adaptar essa verificação.

## 10. Como desativar ou remover

Abra **Opções → Pacotes de recursos**, retire o patch da lista selecionada e confirme. Para removê-lo do disco, feche o jogo e retire apenas o ZIP do patch da pasta `resourcepacks`.

Os arquivos originais do Apocalypse Now, Reanimated Blue e Tissou não são alterados pelo gerador.

Na preparação inicial da instância local, um script separado habilitou o pack no `options.txt` e criou um backup com o padrão `options.txt.before-apocalypse-animations-*.bak`. Esse procedimento local não faz parte do gerador publicado.

## 11. Versionamento e créditos

Os arquivos destinados ao repositório são o código do gerador, a documentação e as regras de exclusão do Git. A pasta `dist` e arquivos `.zip`/`.jar` ficam ignorados no projeto preparado.

O Reanimated Blue e seus modelos/animações pertencem ao respectivo autor, mrblueyeti. Apocalypse Now, EMF, ETF e Tissou’s Zombie Pack pertencem aos respectivos autores.

O ZIP gerado contém modelos derivados do Reanimated. Não foi verificada autorização para redistribuir esses modelos. O fato de o gerador estar no GitHub não concede direitos sobre os arquivos de origem. Confirme as condições aplicáveis antes de disponibilizar o ZIP em releases ou incluí-lo na distribuição pública do modpack.
