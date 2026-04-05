# AcheiUnB

**Número da Lista**: 1<br>
**Conteúdo da Disciplina**: Busca<br>

## Alunos
| Matrícula | Aluno |
| -- | -- |
| 23/1011220  |  Davi Camilo Menezes |
| 23/1026714  |  Euller Júlio da Silva |

## Sobre
O [AcheiUnB](https://github.com/unb-mds/2024-2-AcheiUnB) é um projeto criado para facilitar a busca e a recuperação de itens perdidos na Universidade de Brasília, permitindo que estudantes cadastrem objetos, perdidos ou encontrados, em uma plataforma mais organizada e acessível do que grupos de mensagens informais.

Este trabalho tem como objetivo aprimorar o processo de busca por meio de uma estrutura de índice primário e secundário, baseada no conceito de busca sequencial indexada. A ideia é organizar os itens por uma chave composta `status + categoria + local`, formando blocos de registros. Dentro desses blocos, os itens ficam ordenados por `barcode` ou `data`, permitindo aplicar busca binária, tornando a pesquisa mais rápida e eficiente.

## Screenshots
Adicione 3 ou mais screenshots do projeto em funcionamento.

## Instalação
**Linguagem**: Python<br>
**Framework**: Não foi utilizado<br>
**Pré-requisitos:** Python 3.10+ instalado<br>

### Como rodar

1. Criar e ativar ambiente virtual (recomendado)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

2. Gerar dataset CSV

```bash
python src/generate_dataset.py --rows 5000 --seed 42 --output data/items_benchmark.csv
```

3. Rodar benchmark (sequencial x indexado)

```bash
python src/benchmark_runner.py \
	--csv data/items_benchmark.csv \
	--mode both \
	--iterations 30 \
	--warmup 5 \
	--output results/benchmark_before_after_seed42.json
```

4. Rodar testes do nucleo

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

Se `python` nao estiver disponivel no seu terminal, use `python3` nos comandos acima.

## Uso
Para este projeto de EDA2, o uso principal do nucleo esta no fluxo de validacao:

1. gerar base controlada para experimento
2. medir desempenho antes/depois no mesmo cenario
3. validar corretude com os testes do nucleo

Esse fluxo e o que melhor representa o objetivo do trabalho, pois evidencia o ganho da busca indexada em relacao a busca sequencial.

### Modos de benchmark

- --mode sequential: referencia "antes" (varredura global)
- --mode indexed: referencia "depois" (indice + bloco + binaria/fallback)
- --mode both: gera comparacao direta no mesmo arquivo

### Comparacao de evolucao (print)

Exemplo de resultado com 5000 itens, seed 42, 30 iteracoes:

| Cenario | Sequential avg (ms) | Indexed avg (ms) | Ganho (x) |
| --- | ---: | ---: | ---: |
| key_only_block_scan | 0.9010 | 0.3075 | 2.93x |
| key_plus_barcode | 0.8795 | 0.0032 | 278.37x |
| key_plus_name_filter | 0.9760 | 0.3695 | 2.64x |

```text
[evolucao] key_only_block_scan      0.9010 ms -> 0.3075 ms   (2.93x)
[evolucao] key_plus_barcode         0.8795 ms -> 0.0032 ms (278.37x)
[evolucao] key_plus_name_filter     0.9760 ms -> 0.3695 ms   (2.64x)
```

## Outros
Este repositório não representa o projeto AcheiUnB em si, mas sim o núcleo desacoplado desenvolvido para a disciplina de Estruturas de Dados 2. Sua função é concentrar a implementação da estrutura de busca e indexação de forma separada, facilitando testes, análise e evolução da solução. A integração desse núcleo ao fluxo real do AcheiUnB já foi realizada no repositório do projeto através do seguinte Pull Request:
