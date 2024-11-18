# Projeto de Física - Simulador
<p align="center">
  <img src="assets/diagrama.png" alt="Diagrama representando o modelo físico">
  <br>
  <em>Figura 1: Esquema</em>
</p>


### Foguete
O foguete contém os seguintes atributos:
- Massa (não considera o combustível)
- Posição $\vec{p}$
- Velocidade $\vec{v}$
- Aceleração $\vec{a}$
- Eixo de guinada (ângulo) 
- Motor 

A classe foguete utiliza a classe Motor para gerar o empuxo.
O tipo de motor pode ser especificado

### Motor
O motor contém os seguintes atributos:
- Massa (não considera o combustível)
- Combustível (litros)
- Taxa de queima do combustível

O motor gera empuxo com base em seu peso e na velocidade gerada pela queima do combustível.

A classes de motor que podem ser utilizadas herdam de "RocketEngine" apenas as funções, alterando seus atributos (massa e taxa de queima).
