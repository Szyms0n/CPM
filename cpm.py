import sys
import csv
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt


class CPMApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPM - Critical Path Method")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Wprowadzanie danych (Nazwa → Poprzednicy → Czas)
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Nazwa zadania")
        self.dependencies_input = QLineEdit()
        self.dependencies_input.setPlaceholderText("Poprzednicy (np. ABC)")
        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("Czas trwania")

        self.add_button = QPushButton("Dodaj zadanie")
        self.add_button.clicked.connect(self.add_task)

        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.dependencies_input)
        input_layout.addWidget(self.duration_input)
        input_layout.addWidget(self.add_button)
        self.layout.addLayout(input_layout)

        # Tabela zadań
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Zadanie", "Poprzednicy", "Czas trwania"])
        self.table.itemChanged.connect(self.update_task_from_table)
        self.layout.addWidget(self.table)

        # Przycisk zapisania do CSV
        self.save_button = QPushButton("Zapisz do CSV")
        self.save_button.clicked.connect(self.save_to_csv)
        self.layout.addWidget(self.save_button)

        self.tasks = []

    def add_task(self):
        name = self.task_input.text().strip()
        dependencies = self.dependencies_input.text().strip()
        duration = self.duration_input.text().strip()

        if not name or not duration.isdigit():
            QMessageBox.warning(self, "Błąd", "Podaj poprawną nazwę i czas trwania (liczba całkowita).")
            return

        self.tasks.append((name, dependencies, int(duration)))
        self.update_table()

        self.task_input.clear()
        self.dependencies_input.clear()
        self.duration_input.clear()

    def update_table(self):
        self.table.blockSignals(True)
        self.table.setRowCount(len(self.tasks))
        for row, (name, dependencies, duration) in enumerate(self.tasks):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(dependencies))
            self.table.setItem(row, 2, QTableWidgetItem(str(duration)))
        self.table.blockSignals(False)

    def update_task_from_table(self, item):
        row = item.row()
        col = item.column()
        value = item.text().strip()

        if col == 2 and not value.isdigit():
            QMessageBox.warning(self, "Błąd", "Czas trwania musi być liczbą całkowitą.")
            self.update_table()
            return

        name = self.table.item(row, 0).text().strip()
        dependencies = self.table.item(row, 1).text().strip() if self.table.item(row, 1) else ""
        duration = int(self.table.item(row, 2).text().strip()) if self.table.item(row, 2) else 0

        self.tasks[row] = (name, dependencies, duration)

    def save_to_csv(self):
        if not self.tasks:
            QMessageBox.information(self, "Brak danych", "Brak danych do zapisania.")
            return

        try:
            with open("zadania.csv", mode="w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["ac", "pr", "du"])
                for task in self.tasks:
                    writer.writerow([task[0], task[1], task[2]])
            QMessageBox.information(self, "Zapisano", "Dane zostały zapisane do pliku zadania.csv.")
        except Exception as e:
            QMessageBox.critical(self, "Błąd zapisu", f"Nie udało się zapisać pliku:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CPMApp()
    window.show()
    sys.exit(app.exec())
