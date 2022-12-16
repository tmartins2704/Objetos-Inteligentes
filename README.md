Storage Data IoT - Armazenamento de Dados em Cloud

Este trabalho tem como objetivo propor um protótipo de uma ferramenta IoT que através do protocolo MQTT trocara dados com a nuvem. Protocolo de comunicação este qual traz uma boa alternativa para projetos em IoT uma vez que oferece um poder de processamento mais baixo e uma latência menor. 
Como testes usaremos uma ferramenta que armazena dados em nuvem. É comum que as empresas salvem arquivos importantes em sua rede local, porém conforme ambiente vai crescendo o investimento na camada de hardware se torna caro, fora o fato que o cliente precisará investir muitas vezes em ferramentas de backups e hardware auxiliares tais como (HD Externo, Pen Drive e outros). 
O armazenamento de dados além de elevar o nível de segurança dos clientes, tem como um dos principais objetivos entregar uma redução de custo e um ambiente homogêneo, onde o cliente não precisará se preocupar com investimentos de alto custo.

Em nosso projeto de Storage Data IoT, trabalharemos com o módulo ESP32, LED Difuso Vermelho, Resistor 1K, Kit Jumper Macho, Protobord 400, Carregador Portatil e Cabo USB. Abaixo será especificado as caracteristicas e o papel de cada item neste projeto. 

A placa ESP-WROOM-32 – WiFi Bluetooh é uma placa de desenvolvimento que combina o chip ESP32, uma interface usb-serial e um regulador de tensão 3.3V. A programação será realizada através da IDE do Arduino, utilizando a comunicação via cabo micro-usb.

![image](https://user-images.githubusercontent.com/94072334/208003678-44e23e54-3e47-429d-bda4-ac32d09ec196.png)

Principais características: Certificação ANATEL: 02152-20-11541; Módulo: ESP32-WROOM-32D; Chip Base: ESP32-D0WD; Processador: Xtensa 32-Bit LX6 Dual Core; Clock: 80 à 240 MHz (Ajustável); Memoria ROM: 448KB; Memória SRAM: 520Kb; Memória Flash Externa: 32-Bit de acesso e 4Mb; Tensão de Alimentação: 4,5 à 12,0 VDC (Pino Vin); Tensão de nível lógico: 3,3VDC (não tolera 5V); Corrente de consumo: 80mA (típica); Corrente de consumo: 500mA (máxima); Interfaces: Cartão SD, UART(3 canais), SPI (3 canais), SDIO, I2C (2 canais), I2S (2 canais), IR, PWM LED (2 canais) e PWM motor (3 canais); Tipos GPIO: Digital IO (36), ADC 12-Bits (16 canais), DAC 8-Bits (2 canais), Sensor Capacitivo (10 canais); LNA pré-amplificador; WiFi 802.11 b/g/n: 2.4 à 2.5 GHz; Segurança WiFi: WPA / WPA2 / WPA2-Enterprise / WPS; Criptografia WiFi: AES / RSA / ECC / SHA; Bluetooth 4.2 BR / EDR e BLE (Bluetooth Low Energy); RTC Integrado de 8Kb (Slown / Fast); Sensor integrado: Temperatura e Hall; Temperatura de trabalho: -40° à +85° C; Compatível com a IDE do Arduino; Dimensões: 27,5 x 51,0 x 7,0 mm; ESP32 Pinout: 30 Pinos.
Utilizaremos 1 LED (Light Emitting Diodo) Difuso 5mm. O equipamento é formado por um material semicondutor, que emite luz quando uma tensão é aplicada aos seus terminais.
 
![image](https://user-images.githubusercontent.com/94072334/208003707-8c647020-6dd8-403b-9ec7-30aac71691c7.png)

Resistor 1K - 1/4W - 5% é um componente eletrônico utilizado em circuitos como forma de limitar a corrente elétrica, provocar queda de tensão e gerar calor.

 ![image](https://user-images.githubusercontent.com/94072334/208003715-ba646c8f-b6f9-49b0-9e11-68e4e7ef9a84.png)

Figura 3. Resistor 1K - 1/4W - 5%. Fonte: Mercado Livre

Principais Características: Resistência: 1K; Potência: 1/4 Watts; Calor: 1/4 J/s (1/4 Joule por segundo); Tolerância: ±5%; Faixa de cores: marrom, preto, vermelho, dourado; Modelo: CR25

 
O Kit Jumper Macho, será utilizado para efetuar as conexões entre componentes eletrônicos e em uma das extremidades do cabo o conector é macho e na outra extremidade é macho. Os cabos são divididos em 10 cores diferentes o que facilita identificar as conexões do nosso projeto.
 
![image](https://user-images.githubusercontent.com/94072334/208003744-ca7ff068-f756-445e-bf68-0eb4a63d39e2.png)

Os Cabos Jumper são fios de ligação elétrica, ideias e indispensável para quem faz montagens com Placa Arduino, Protoboard, Shield Arduino e os mais diversos Módulos, assim como para outras plataformas de desenvolvimento.
Principais Características: Tipo: Macho x Macho; Quantidade: 65 peças; Comprimento do Cabo: 11, 15, 20 e 24 cm; Secção do condutor: 24 AWG (0,2 mm²); Condutores totalmente revestidos; Diferenciado por 6 cores de forma sortida; Cores: Vermelho, Laranja, Amarelo, Verde, Azul e Preto; Produto 100% industrializado; Peso: 32 gramas

 
A Montagem dos circuitos eletrônicos, será realizada utilizando o Protoboard, que possui 400 pontos e em sua parte inferior e há um adesivo que permite colá-lo em uma superfície isolante. São 100 pontos de distribuição e 300 pontos de conexão terminal. Possuindo coordenadas coloridas para facilitar a visualização dos componentes. As duas ilhas centrais são destinadas a receber os componentes que serão utilizados no circuito que está sendo montado. As colunas em uma mesma linha estão ligadas entre si. Dessa forma, dois ou mais componentes que precisam estar conectados devem ter os seus terminais ocupando uma mesma coluna. As linhas, por sua vez, não apresentam conexão entre si. Um mesmo componente nunca pode ter os seus terminais ocupando uma mesma coluna de uma mesma ilha, pois, dessa forma, seus terminais sempre estarão com um mesmo potencial, a corrente elétrica não fluirá́ e o componente não funcionará
 
![image](https://user-images.githubusercontent.com/94072334/208003778-3c661b5c-094f-4c9a-97d6-2ee5f254b43b.png)

Protoboard, também conhecida como Breadboard, Placa de Ensaio ou Matriz de Contato, é uma placa com furos e conexões pré-definidas, que visa auxiliar a montagem de teste de circuitos eletrônicos experimentais de forma simples e ágil.
Principais Características: Quantidade de pontos: 400; Barramento de alimentação: 2 pares (+ e -); Material Base: ABS; Material de conexão: Bronze banhado à Níquel; terminais suportados: 0,3 à 0,8 mm²; Resistencia de isolamento: 100 MΩ / min; Tensão Máxima: 500 VAC / min; Dimensões: 83mm x 55mm x 10mm; Peso: 30 gramas.

Para trabalhar como nossa fonta de aliminetação, via rede elétrica optei por um carregador externo tradicionao. Utilizando um carregador com um cabo micro Usb (v8) 2.0. Voltagem: 5V | Bivolt. Amperagem:2ª | Conexão: Micro USB.

 ![image](https://user-images.githubusercontent.com/94072334/208003599-64fde9ff-7842-460f-98b2-c9a542fadf5d.png)
 
 Fonte Ideia: https://conaenge.com.br/esp32-publicando-dados-na-nuvem-google/
 
 Prototipagem: 

![image](https://user-images.githubusercontent.com/94072334/208004180-ea4d0c87-3411-41c1-81d4-163f60c6c39c.png)

