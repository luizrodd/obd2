import obd
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QApplication, QComboBox, QPushButton, 
    QHBoxLayout, QListWidget, QListWidgetItem, QCheckBox
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QIcon
from commands import OBDCommands  # Certifique-se de que o arquivo commands.py contém o Enum OBDCommands

class OBDMonitor(QWidget):
    def __init__(self, connection):
        super().__init__()

        self.connection = connection
        self.comandos_disponiveis = {cmd.label: cmd.command for cmd in OBDCommands}
        self.comandos_selecionados = {}

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Monitor OBD-II")
        self.setGeometry(100, 100, 400, 500)

        self.layout = QVBoxLayout()

        # Dropdown com seleção múltipla
        self.combo = QListWidget()
        self.combo.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.combo.addItems(OBDCommands.get_labels())
        self.layout.addWidget(self.combo)

        # Botão para adicionar os itens selecionados
        self.btn_add = QPushButton("Adicionar Selecionados")
        self.btn_add.clicked.connect(self.add_params)
        self.layout.addWidget(self.btn_add)

        # Lista para exibir os dados monitorados
        self.lista_parametros = QListWidget()
        self.layout.addWidget(self.lista_parametros)

        self.setLayout(self.layout)

        # Atualização automática dos dados
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Atualiza a cada segundo

    def add_params(self):
        """Adiciona múltiplos parâmetros ao monitoramento"""
        itens_selecionados = self.combo.selectedItems()

        for item in itens_selecionados:
            nome = item.text()
            comando = OBDCommands.get_by_label(nome)

            if nome not in self.comandos_selecionados and comando:
                self.comandos_selecionados[nome] = comando
                self.add_param_item(nome)

    def add_param_item(self, nome):
        """Adiciona um item individual à lista de monitoramento"""
        item = QListWidgetItem()
        widget_item = QWidget()
        layout_h = QHBoxLayout()

        # Criar label para exibir o dado
        label = QLabel(f"{nome}: ---")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Botão para remover
        btn_remove = QPushButton()
        btn_remove.setIcon(QIcon.fromTheme("edit-delete"))  # Ícone de lixeira
        btn_remove.setFixedSize(30, 30)
        btn_remove.clicked.connect(lambda _, n=nome, i=item: self.remove_param(n, i))

        layout_h.addWidget(label)
        layout_h.addWidget(btn_remove)
        layout_h.setContentsMargins(5, 5, 5, 5)
        widget_item.setLayout(layout_h)

        item.setSizeHint(widget_item.sizeHint())
        self.lista_parametros.addItem(item)
        self.lista_parametros.setItemWidget(item, widget_item)

    def remove_param(self, nome, item):
        """Remove um parâmetro do monitoramento"""
        if nome in self.comandos_selecionados:
            del self.comandos_selecionados[nome]

        row = self.lista_parametros.row(item)
        self.lista_parametros.takeItem(row)

    def update_data(self):
        """Atualiza os valores dos parâmetros selecionados"""
        for index in range(self.lista_parametros.count()):
            item = self.lista_parametros.item(index)
            widget = self.lista_parametros.itemWidget(item)

            if widget:
                layout = widget.layout()
                label = layout.itemAt(0).widget()
                nome = label.text().split(":")[0]  # Nome do parâmetro

                comando = self.comandos_selecionados.get(nome)
                if comando:
                    response = self.connection.query(comando)
                    if not response.is_null():
                        label.setText(f"{nome}: {response.value}")

