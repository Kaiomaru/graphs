#!/usr/bin/python3
#-*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QGridLayout, QLabel, QErrorMessage, QCheckBox, QMessageBox, QTableWidget
import networkx as nx 
import matplotlib.pyplot as plt 
import random
import queue
import numpy as np
import math
import itertools

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.g = nx.Graph()
        self.errorMsg = QErrorMessage()
        self.errorMsg.setFixedSize(500, 220)
        self.messageBox = QMessageBox()
        self.messageBox.setFixedSize(500, 220)


    #Инициация графического интерфейса: создание и расположение элементов в сетке
    def initUI(self):
        self.setGeometry(875, 700, 450, 300)
        self.setWindowTitle('Graph working')

        grid = QGridLayout()
        grid.setSpacing(10)

        addNodeBtn = QPushButton('Add node', self)
        addNodeBtn.clicked.connect(self.AddNode)
        
        createBtn = QPushButton('Create', self)  
        createBtn.clicked.connect(self.Create)

        addRelationBtn = QPushButton('Add relation', self)
        addRelationBtn.clicked.connect(self.AddRelation)

        delRelButton = QPushButton('Delete')
        delRelButton.clicked.connect(self.DeleteRelation)

        delVertButton = QPushButton('Delete')
        delVertButton.clicked.connect(self.DeleteVertex)

        runFordBtn = QPushButton('Fords alg', self)
        runFordBtn.clicked.connect(self.RunFordAlg)

        runShimbBtn = QPushButton('Shimbell alg', self)
        runShimbBtn.clicked.connect(self.RunShimbellAlg)

        self.isDirectedChckBx = QCheckBox('Directed')
        self.isDirectedChckBx.stateChanged.connect(self.ChangedGraph)

        self.relFrom = QLineEdit(self)   
        self.relFrom.setPlaceholderText('From')
        self.relTo= QLineEdit(self)
        self.relTo.setPlaceholderText('To')
        self.vertCount = QLineEdit(self)
        self.vertCount.setPlaceholderText('Vertex count')
        self.relCount = QLineEdit(self)
        self.relCount.setPlaceholderText('Relation count')
        self.weight = QLineEdit(self)
        self.weight.setPlaceholderText('Weight')
        self.delRelFrom = QLineEdit()
        self.delRelFrom.setPlaceholderText('From')
        self.delRelTo = QLineEdit()
        self.delRelTo.setPlaceholderText('To')
        self.delVertNumb = QLineEdit()
        self.delVertNumb.setPlaceholderText('Number')
        self.fordStartVertex = QLineEdit(self)
        self.fordStartVertex.setPlaceholderText('Start')
        self.heldStartVertex = QLineEdit(self)
        self.heldStartVertex.setPlaceholderText('Start')

        delRelLabel = QLabel('Delete relation')
        delVertLabel = QLabel('Delete vertex')
        relAddingLabel = QLabel('Add relation')


        showBtn = QPushButton('Show', self)
        showBtn.clicked.connect(self.Show)
        showBtn.setFixedSize(120, 50)


        grid.addWidget(self.vertCount, 1, 1)
        grid.addWidget(createBtn, 1, 3)
        grid.addWidget(self.relCount,1, 2)
        grid.addWidget(addNodeBtn, 1, 4)

        grid.addWidget(delVertLabel, 2, 1)
        grid.addWidget(self.delVertNumb, 2, 2)
        grid.addWidget(delVertButton, 2, 3)

        grid.addWidget(delRelLabel, 3, 1)
        grid.addWidget(self.delRelFrom, 3, 2)
        grid.addWidget(self.delRelTo, 3, 3)
        grid.addWidget(delRelButton, 3, 4)
        
        grid.addWidget(relAddingLabel, 4, 1, 2, 1)
        grid.addWidget(self.relFrom, 4, 2)
        grid.addWidget(self.weight, 4, 3, 2, 1)
        grid.addWidget(addRelationBtn, 4, 4, 2, 1)
  
        grid.addWidget(self.relTo, 5, 2)

        grid.addWidget(self.isDirectedChckBx, 6, 2)
        grid.addWidget(showBtn, 6, 4)

        grid.addWidget(self.fordStartVertex, 7, 1)
        grid.addWidget(runFordBtn, 7, 2)
        grid.addWidget(runShimbBtn, 7, 3)

        grid.addWidget(self.heldStartVertex, 8, 4)

        self.setLayout(grid)

        self.show() 


    #Добавить вершину с номером n+1 в граф
    def AddNode(self):
        self.g.add_node(self.g.number_of_nodes() + 1)


    #Показать граф в новом окне matplotlib
    def Show(self):
        plt.close()

        #Получаем веса ребер
        edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in self.g.edges(data=True)])
        #Формируем позиции вершин
        pos=nx.spring_layout(self.g)

        nx.draw_networkx_edge_labels(self.g, pos, edge_labels=edge_labels)
        nx.draw(self.g, pos, with_labels=True)

        plt.show(block=False)


    #Добавление связи
    def AddRelation(self):
        from_ = self.relFrom.text()
        to_ = self.relTo.text()

        try:
            if not str.isdigit(from_):
                raise Exception('Введите вершину "Откуда" - положительное целое число')
            if not str.isdigit(to_):
                raise Exception('Введите вершину "Куда" - положительное целое число')

            weight_ = int(self.weight.text())

            if weight_ == 0:
                raise Exception('Вес должен быть положительным числом')

            #Переворачивание стрелки, если вес отрицательный
            if weight_ < 0:
                weight_ = -weight_
                temp = from_
                from_=to_
                to_=temp

            self.g.add_edge(int(from_), int(to_), weight=weight_)

        except ValueError:
            self.errorMsg.showMessage('Введите вес - целое число')
        except Exception as e:
            self.errorMsg.showMessage(e.args[0])


    #Создание нового случайного графа с определенным кол-вом вершин и связей
    def Create(self):
        self.g.clear()
        try:
            if not str.isdigit(self.vertCount.text()):
                raise Exception('Введите целочисленное положительное количество вершин')
            if not str.isdigit(self.relCount.text()):
                raise Exception('Введите челочисленное положительное количество связей')
            
            vertexNumb = int(self.vertCount.text())
            relationNumb = int(self.relCount.text())

            for i in range(1, vertexNumb+1):
                self.g.add_node(i)
            for i in range(1, relationNumb+1):
                #Генерим случайные числа - ребра нашего графа
                from_, to_ = random.randint(1, self.g.number_of_nodes()),\
                            random.randint(1, self.g.number_of_nodes())

                #Если получилась петля или уже дублирующая связь(вне зависимости от направления), меняем числа
                while from_ == to_ or to_ in list(self.g.adj[from_]) or from_ in list(self.g.adj[to_]):
                    from_, to_ = random.randint(1,self.g.number_of_nodes()),\
                                random.randint(1,self.g.number_of_nodes())

                    if vertexNumb*(vertexNumb-1)/2 < relationNumb:
                        raise Exception('Столько уникальных ребер не может быть при указанном количестве вершин')

                randWeight = random.randint(1, 10)
                self.g.add_edge(from_, to_, weight=randWeight)
            
            matrix = np.zeros((self.g.number_of_nodes(), self.g.number_of_nodes()))

            for node_from in self.g.nodes():
                for node_to in self.g.nodes():
                    if node_to in self.g.adj[node_from]:
                        matrix[node_from-1][node_to-1] = self.g[node_from][node_to]['weight']
            

        except Exception as e:
            self.errorMsg.showMessage(e.args[0])

    
    #Удаление связи, если она существует в грфае
    def DeleteRelation(self):
        from_ = self.delRelFrom.text()
        to_ = self.delRelTo.text()
        try:
            if not str.isdigit(from_):
                raise Exception('Введите вершину "Откуда" - положительное целое число')
            if not str.isdigit(to_):
                raise Exception('Введите вершину "Куда" - положительное целое число')
            if int(from_) not in self.g.nodes() or (int(from_), int(to_)) not in self.g.edges():
                raise Exception('Такой связи не существует')

            self.g.remove_edge(int(from_), int(to_))

        except Exception as e:
            self.errorMsg.showMessage(e.args[0])


    #Удаление вершины
    def DeleteVertex(self):
        deleteNumber = self.delVertNumb.text()
        try:
            if not str.isdigit(deleteNumber):
                raise Exception('Введите номер удаляемой вершины - положительное целое число')
            if not int(deleteNumber) in self.g.nodes():
                raise Exception('Такой вершины не существует')

            self.g.remove_node(int(deleteNumber))
            
        except Exception as e:
            self.errorMsg.showMessage(e.args[0])


    #Если изменили тип графа в чекбоксе
    def ChangedGraph(self):
        if self.isDirectedChckBx.isChecked:
            self.g = nx.DiGraph() #Создаем новые графы
        else:
            self.g = nx.Graph()


    #Алгоритм Форда для поиска кратчайшего пути от одной вершины до остальных
    def RunFordAlg(self):      
        try:
            if not str.isdigit(self.fordStartVertex.text()):
                raise Exception('Введите номер вершины - положительное целое число')
            
            start = int(self.fordStartVertex.text())

            if int(self.fordStartVertex.text()) not in self.g.nodes():
                raise Exception('Такой вершины не существует')

            distances = {}
            distances[str(start)] = 0

            q = queue.Queue()
            q.put(start)
            nodes = list(self.g.nodes())

            while not q.empty():              
                current_node = q.get()
                nodes.remove(current_node)
                for neighbour in list(self.g.adj[current_node]):                   
                    new_dist = distances[str(current_node)] + self.g[current_node][neighbour]['weight']
                    if neighbour in nodes and not neighbour in q.queue:
                        q.put(neighbour)
                        distances[str(neighbour)] = new_dist
                    else:
                        if new_dist < distances[str(neighbour)]:
                            distances[str(neighbour)] = new_dist

            text = ''
            for key in distances.keys():
                text = text + 'Путь до ' + str(key) + ' = ' + str(distances[key]) + '\n'
            self.messageBox.setText(text)
            self.messageBox.show()

        except Exception as e:
            self.errorMsg.showMessage(e.args[0])      


    #Алгоритм Шимбелла до длины пути - размерность графа -1
    def RunShimbellAlg(self):
        matrix = np.zeros((self.g.number_of_nodes(), self.g.number_of_nodes()))

        for node_from in self.g.nodes():
            for node_to in self.g.nodes():
                if node_to in self.g.adj[node_from]:
                    matrix[node_from-1][node_to-1] = self.g[node_from][node_to]['weight']

        result = matrix
        
        str_result = str(result)
        str_result += "\n------------------------1-------------------------\n"

        for i in range(0,len(matrix-1)):
            result = self.MatrixMultiply(matrix, result)
            str_result += str(result) + "\n-------------------------{}-------------------------\n".format(i + 2)
        
        self.messageBox.setText(str_result)
        self.messageBox.show()
        

    #Умножение матриц (по Шимбеллу)
    #строка на столбец. если один из слагаемых - 0, отбрасываем
    #если путей несколько, берем минимум
    def MatrixMultiply(self, matrix1, matrix2):
        res = np.zeros((len(matrix1), len(matrix1)))

        for i in range(0,len(res)):
            for j in range(0,len(res)):
                sum = 0
                terms = []
                for k in range(0,len(res)):
                    if matrix1[i][k] != 0 and matrix2[k][j] != 0:
                        terms.append(matrix1[i][k] + matrix2[k][j])
                if len(terms)>0:
                    res[i][j] = min(terms)

        return res

    def print_mtrx(self, matrix):
        for i in range(0, len(matrix)):
            print(matrix[i])

    def redux(self, matrix):
        row_mins = []
        col_mins = []
        for i in range(0, len(matrix)):
            row_mins.append(min(matrix[i]))
            for j in range(0, len(matrix)):
                matrix[i,j]-=row_mins[i]

        for j in range(0, len(matrix)):
            col_mins.append(min(matrix[:,j]))
            for i in range(0, len(matrix)):
                matrix[i,j]-=col_mins[j]
        return matrix, row_mins, col_mins



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())