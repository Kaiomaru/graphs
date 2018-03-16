from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QGridLayout, QLabel, QErrorMessage, QCheckBox, QMessageBox, QTableWidget
import networkx as nx
import math

class ResourcesWindow(QWidget):
    def __init__(self, g):
        super().__init__()
        self.g = g
        self.errorMsg = QErrorMessage()
        self.errorMsg.setFixedSize(500,220)
        self.messageBox = QMessageBox()
        self.messageBox.setFixedSize(500,220)
        self.initUI()

    def initUI(self):
        self.setGeometry(850,200,550,200)
        self.setWindowTitle('Resources')

        self.table = QTableWidget()
        self.table.setRowCount(2)
        self.table.setVerticalHeaderLabels(['bj', 'Tj'])
        self.table.setColumnCount(len(self.g.nodes()))

        self.groupCount = QLineEdit()
        self.groupCount.setPlaceholderText('Group count')

        runBtn = QPushButton('Run')
        runBtn.clicked.connect(self.Run)

        grid = QGridLayout()
        grid.setSpacing(10)
        self.setLayout(grid)

        grid.addWidget(self.table, 1, 1, 1, 6)
        grid.addWidget(self.groupCount, 2, 2, 1, 2)
        grid.addWidget(runBtn, 2, 4, 1, 2)
        self.show()

    def Run(self):
        nodes = self.g.nodes()
        bs = []
        ts = []
        try:
            group_count = int(self.groupCount.text())
        except ValueError:
            self.errorMsg.showMessage("Введите корректное число бригад")
            return
        try:
            for i in range(0, len(nodes)):
                bs.append(int(self.table.item(0, i).text()))     #Штрафы в хородах
                ts.append(int(self.table.item(1, i).text()))     #Время ремонта
        except AttributeError:
            self.errorMsg.showMessage("Заполните все клетки таблицы")
            return

        shortest_paths = []             #Кратчайшие пути между городами
        for i in range(0, len(nodes)):
            shortest_paths.append([])
            for j in range(0, len(nodes)):
                shortest_paths[i].append(nx.shortest_path_length(self.g, source=i+1, target=j+1, weight='weight'))

        evaluation = []
        for i in range(0, len(nodes)):          #Считаем матрицу оценок
            evaluation.append([])
            for j in range(0, len(nodes)):
                if i == j:
                    evaluation[i].append(int(bs[i]) / int(ts[i]))
                else:
                    evaluation[i].append(int(bs[i]) / (int(ts[i]) + shortest_paths[i][j]))  

        paths = []
        taus = []
        city_left = len(self.g.nodes()) % (2 * group_count)

        for k in range(0, group_count):
            paths.append([])
            max_ = 0
            index = -1

            for i in range(0, len(nodes)):
                if evaluation[i][i] > max_:
                    max_ = evaluation[i][i]
                    index = i

            second_max = max(evaluation[index][:index:])
            second_index = evaluation[index].index(second_max)

            paths[k].append(index)
            paths[k].append(second_index)

            #Считаем тау для двух городов у каждой бригады
            tau_value = evaluation[index][second_index] * ts[index] + shortest_paths[index][second_index] + ts[second_index]
            taus.append(tau_value)

            for i in range(0, len(evaluation)):
                evaluation[index][i] = 0
                evaluation[i][second_index] = 0
                evaluation[i][index] = 0
                evaluation[i][second_index] = 0

        left = []
        for city in self.g.nodes():
            city = city-1
            having = False
            for i in range(0, len(paths)):          #Помещаем оставшиеся города в отдельный массив       
                if city in paths[i] or city in left:
                    having = True
            if not having:
                left.append(city)

        print(left)

        while city_left > 0:        #Распределяем оставшиеся города
            for i in range(0, group_count):
                print(taus)
                min_ = math.inf
                index_path = -1
                index_city = -1
                paths_end = paths[i][len(paths[i])-1]

                current_group_tau = taus[i] + shortest_paths[paths_end][left[city_left-1]] + ts[left[city_left-1]]
                if current_group_tau < min_:
                    min_ = current_group_tau
                    index_path = i
            paths[index_path].append(left[city_left-1])
            taus[index_path] += min_
            city_left-=1
            print(min_)
        print(paths)
        text = ""
        for i in range(0, len(paths)):
            text+=str(i)+" бригада:"
            for j in range(0, len(paths[i])):
                text+=str(paths[i][j]+1)
                text+= " "
            text+="\n"
        self.messageBox.setText(text)
        self.messageBox.show()
