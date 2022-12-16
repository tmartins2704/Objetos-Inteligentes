Storage Data IoT - Armazenamento de Dados em Cloud

Este trabalho tem como objetivo propor um protótipo de uma ferramenta IoT que através do protocolo MQTT trocara dados com a nuvem. Protocolo de comunicação este qual traz uma boa alternativa para projetos em IoT uma vez que oferece um poder de processamento mais baixo e uma latência menor. 
Como testes usaremos uma ferramenta que armazena dados em nuvem. É comum que as empresas salvem arquivos importantes em sua rede local, porém conforme ambiente vai crescendo o investimento na camada de hardware se torna caro, fora o fato que o cliente precisará investir muitas vezes em ferramentas de backups e hardware auxiliares tais como (HD Externo, Pen Drive e outros). 
O armazenamento de dados além de elevar o nível de segurança dos clientes, tem como um dos principais objetivos entregar uma redução de custo e um ambiente homogêneo, onde o cliente não precisará se preocupar com investimentos de alto custo.

Para entrega do meu trabalho, estou considerando as ferramentas: 

A placa ESP-WROOM-32 – WiFi Bluetooh:

![image](https://user-images.githubusercontent.com/94072334/208003678-44e23e54-3e47-429d-bda4-ac32d09ec196.png)

1 LED (Light Emitting Diodo) Difuso 5mm:

![image](https://user-images.githubusercontent.com/94072334/208003707-8c647020-6dd8-403b-9ec7-30aac71691c7.png)

Resistor 1K - 1/4W - 5%:

 ![image](https://user-images.githubusercontent.com/94072334/208003715-ba646c8f-b6f9-49b0-9e11-68e4e7ef9a84.png)
 
Kit Jumper Macho:
 
![image](https://user-images.githubusercontent.com/94072334/208003744-ca7ff068-f756-445e-bf68-0eb4a63d39e2.png)

Protoboard 400 Pontos:
 
![image](https://user-images.githubusercontent.com/94072334/208003778-3c661b5c-094f-4c9a-97d6-2ee5f254b43b.png)

Carregador Portatil Eletrico

 ![image](https://user-images.githubusercontent.com/94072334/208003599-64fde9ff-7842-460f-98b2-c9a542fadf5d.png)
 
 Como inspiração da minha ideia, compartilho o link: https://conaenge.com.br/esp32-publicando-dados-na-nuvem-google/
 
 Prototipagem:

![image](https://user-images.githubusercontent.com/94072334/208004180-ea4d0c87-3411-41c1-81d4-163f60c6c39c.png)

Modo de Entrega: 
     Para configuração deste projeto, trabalharemos com serviço em cloud IBM Cloud, onde será criado o servidor ao qual receberá as informações via MQTT e o IBM Watson onde será realizado a configuração do Node-Red para operar junto com nosso dispositivo ESP32. 
     
     Além das ferramentas ora descrita acima, também será necessário criar uma conta IBM Cloud, um cartão de crédito. 
     Detalhes de configuração serão descritas no trabalho em word entregue ao professor. 
