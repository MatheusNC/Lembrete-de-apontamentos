# Appointment Reminder

Este é um aplicativo simples de lembrete de apontamentos. Ele foi desenvolvido usando a linguagem de programação Python.

## Requisitos

Certifique-se de ter o Python instalado em seu sistema antes de executar este aplicativo.

## Melhoria (Windows)

Altere o caminho do arquivo run.BAT para o caminho do seu arquivo 'main.py' ```python -u "seu_caminho\main.py"```

É possível executar o programa de forma recorrente, você terá que abrir o "Agendador de Tarefas" e criar uma nova tarefa. Quando for selecionar qual arquivo deseja executar, use o run.BAT

## Como executar

1. É possível alterar o caminho de onde o banco de dados será criado. Altere os caminhos "./db" para o caminho desejado.

    ```python
    if os.path.exists("./db"):
            print("Conectando ao banco...")
            self.connect = sqlite3.connect("./db/database.sqlite")
            self.cursor = self.connect.cursor()
        else:
            print("Banco de dados não encontrado")
            print("Criando banco de dados...")
            os.mkdir("./db")
            self.connect = sqlite3.connect("./db/database.sqlite")
            self.cursor = self.connect.cursor()
    ```

1. Abra o terminal e navegue até o diretório do projeto.
2. Execute o seguinte comando para iniciar o aplicativo:

    ```bash
    python app/main.py
    ```

Isso é tudo! Agora você pode usar este README.md como um guia para entender e executar o código em app/main.py.