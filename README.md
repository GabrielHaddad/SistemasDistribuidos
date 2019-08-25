# SistemasDistribuidos
Projeto de Sistemas Distribuidos para matéria de SD

#Descrição do Projeto
Projeto inicialmente se baseia em um aplicativo de chat ao estilo do Whatsapp,
onde poderão ter conversas privadas entre duas pessoas ou criação de grupos
com mais pessoas.
Terá alguns clientes que irão se conectar ao servidor e começaram a conversa.

#Testes a serem implementados
Para um projeto de chat com várias pessoas é indispensável um teste de concorrência
na qual criando um grupo com várias pessoas ao mesmo tempo, o serviço ocorra normal
mente.

Recuperação de falhas: Em uma conversa, se alguma das partes tiver problemas no
serviço, não influenciar no grupo e ela conseguir voltar normalmente para a conversa.

Demonstração de funcionalidades: Como se trata de um chat, para demonstrar as 
funcionalidades funcionando como devem, irei implementar a criação de uma 
conversa simples entre duas pessoas, criação de grupos com mais de duas pessoas,
sair e voltar de conversas sem problemas.