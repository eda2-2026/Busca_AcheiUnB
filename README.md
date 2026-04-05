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

Descreva os pré-requisitos para rodar o seu projeto e os comandos necessários.

## Uso
Explique como usar seu projeto caso haja algum passo a passo após o comando de execução.

## Outros
Este repositório não representa o projeto AcheiUnB em si, mas sim o núcleo desacoplado desenvolvido para a disciplina de Estruturas de Dados 2. Sua função é concentrar a implementação da estrutura de busca e indexação de forma separada, facilitando testes, análise e evolução da solução. A integração desse núcleo ao fluxo real do AcheiUnB já foi realizada no repositório do projeto através do seguinte Pull Request:
