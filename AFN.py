import graphviz

class AFN():

    def __init__(self, estado_inicial, alfabeto = [], estados = [], estados_de_aceptacion = [], transitions = {}, estado_final = None) -> None:
        
        self.estado_final = estado_final
        self.alfabeto: list = alfabeto #Aceptado como trancisiones (nombre de arista, digamos)
        self.estados: list = estados #Estados (vertices)
        self.estado_inicial = estado_inicial
        self.estados_de_aceptacion: list = [item for item in estados_de_aceptacion if item in self.estados]

        self.transitions: dict = transitions if transitions else {estado: {caracter: [] for caracter in self.alfabeto} for estado in self.estados}#Trancisiones que se realizan entre (representa las aristas), Vertical:  // None indica que no hay trancision
        self.hasTransitionE: bool = 'ε' in self.alfabeto 
        self.cerraduras_de_estados = { estado : set() for estado in self.estados }
        self.caminos = []


    def draw_afn(self):
        afn = graphviz.Digraph(format='pdf')
        afn.graph_attr['rankdir'] = 'LR'
        afn.node('start', style='invis')
        for state in self.estados:
            if state==self.estado_inicial:
                afn.node(state, shape='diamond', color='red')
            elif state not in self.estados_de_aceptacion:
                afn.node(state)
            else:
                afn.node(state, shape='doublecircle')
            
        for state in self.transitions:
            trans = self.transitions.get(state)
            for symbol in trans:
                transitions = trans.get(symbol)
                if transitions!=None:
                    for next_state in transitions:
                        afn.edge(state, next_state, label=symbol)

        afn.render('afn', view=True)