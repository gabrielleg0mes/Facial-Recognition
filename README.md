## Reconhecimento Facial com AWS Rekognition e Bedrock

### Descrição
Este projeto utiliza o Amazon Rekognition para análise e extração de tags de imagens e o Amazon Bedrock para gerar conteúdos personalizados com base nas informações extraídas, proporcionando insights automatizados sobre dados visuais.

### Índice
1. [Visão Geral](#visão-geral)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Pré-requisitos](#pré-requisitos)
4. [Instalação e Configuração](#instalação-e-configuração)
5. [Requisições POST](#requisições-post)
6. [Dificuldades Encontradas](#dificuldades-encontradas)
7. [Conclusão](#conclusão)
8. [Autores](#autores)

### Visão Geral
O objetivo deste sistema é identificar e classificar automaticamente objetos e emoções em imagens, gerando insights que podem ser utilizados para diferentes finalidades, como recomendações baseadas em dados visuais.

### Estrutura do Projeto

```
visao-computacional/
├── handlers/                       # Funções de manipulação de eventos
│   ├── v1_vision_handler.py        # Handler da rota /v1/vision
│   ├── v2_vision_handler.py        # Handler da rota /v2/vision
├── services/                       # Serviços AWS
│   ├── bedrock_service.py          # Interação com Amazon Bedrock
│   ├── rekognition_service.py      # Interação com Amazon Rekognition
│   ├── s3_service.py               # Interação com Amazon S3
│   ├── .env                        # Variáveis de ambiente (não incluso no controle de versão)
│   ├── handler.py                  # Handler principal
│   ├── requirements.txt            # Dependências do projeto
│   ├── serverless.yml              # Configurações do Serverless Framework
└── assets/                         # Arquivos estáticos
```

### Pré-requisitos
- [Python 3.10](https://www.python.org/downloads/)
- [AWS CLI](https://aws.amazon.com/cli/) configurado com credenciais válidas
- [Serverless Framework](https://www.serverless.com/framework/docs/getting-started/)
- Acesso à conta da AWS com permissões para os serviços utilizados (Rekognition, S3, Bedrock)

### Instalação e Configuração

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Compass-pb-aws-2024-JULHO-A/sprint-8-pb-aws-julho-a.git
   cd sprint-8-pb-aws-julho-a
   ```

2. **Instale o Serverless Framework:**
   ```bash
   npm install -g serverless
   ```

3. **Instale o AWS CLI v2:**
   - **Windows**:
     ```bash
     msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
     ```
   - **Linux**:
     ```bash
     curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
     unzip awscliv2.zip
     sudo ./aws/install
     ```

4. **Configure as credenciais da AWS:**
   ```bash
   aws configure
   ```

5. **Realize o deploy da aplicação:**
   ```bash
   serverless deploy
   ```

### Modelo de requisição
Após o deploy, você pode testar a aplicação utilizando as rotas da API para extração de tags e análise de emoções em imagens.

- **Para extrair tags de uma imagem:**
   ```bash
   curl -X POST https://your-api-endpoint/v1/vision -H "Content-Type: application/json" -d '{
      "bucket": "nome-do-bucket",
      "imageName": "nome-da-imagem.jpeg"
   }' 
   ```

- **Para análise de emoções em uma imagem:**
   ```bash
   curl -X POST https://your-api-endpoint/v2/vision -H "Content-Type: application/json" -d '{
      "bucket": "nome-do-bucket",
      "imageName": "nome-da-imagem.jpeg"
   }'
   ```

### Modelo de Resposta
Para uma requisição bem-sucedida para a análise de emoções, a resposta pode ser:

```json
{
    "url_to_image": "https://example.com/image.jpg",
    "created_image": "2024-10-26T02:39:46+00:00",
    "faces": {
        "emotion": "CALM",
        "confidence": 96.861
    },
    "pets": [
        {
            "Name": "Dog",
            "Confidence": 93.613,
            "Dicas": "Cuidados: escove a pelagem regularmente."
        }
    ]
}
```

### Dificuldades Encontradas
- Integração entre o AWS Rekognition e Bedrock para gerar insights sobre pets.
- Configuração de permissões detalhadas no Serverless Framework.

### Conclusão
Este projeto demonstrou como a arquitetura serverless, junto com os serviços da AWS, pode ser utilizada para automatizar a análise de imagens de forma eficiente. Com o Amazon Rekognition e o Amazon Bedrock, conseguimos criar um sistema de análise e geração de conteúdo aplicável em várias áreas. Este sistema é escalável e pode ser aprimorado no futuro para atender a mais necessidades, contribuindo para o aprendizado em soluções de IA e computação serverless.

### Autores

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/gabrielleg0mes">
        <img src="https://avatars.githubusercontent.com/u/92538624?v=4" width="120" alt="Gabrielle Souza" style="border-radius: 50%;">
      </a>
      <p><strong>Gabrielle Souza</strong></p>
      <a href="https://github.com/gabrielleg0mes">Perfil no GitHub</a>
    </td>
    <td align="center">
      <a href="https://github.com/Maehh">
        <img src="https://avatars.githubusercontent.com/u/103941673?v=4" width="120" alt="Gustavo Eliel" style="border-radius: 50%;">
      </a>
      <p><strong>Gustavo Eliel</strong></p>
      <a href="https://github.com/Maehh">Perfil no GitHub</a>
    </td>
    <td align="center">
      <a href="https://github.com/hellenilda">
        <img src="https://avatars.githubusercontent.com/u/109177631?v=4" width="120" alt="Hellen Lima" style="border-radius: 50%;">
      </a>
      <p><strong>Hellen Lima</strong></p>
      <a href="https://github.com/hellenilda">Perfil no GitHub</a>
    </td>
    <td align="center">
      <a href="https://github.com/vambertojunior">
        <img src="https://avatars.githubusercontent.com/u/40028930?v=4" width="120" alt="Vamberto Junior" style="border-radius: 50%;">
      </a>
      <p><strong>Vamberto Junior</strong></p>
      <a href="https://github.com/vambertojunior">Perfil no GitHub</a>
    </td>
  </tr>
</table>