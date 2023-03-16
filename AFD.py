import graphviz

class AFD():

    def __init__(self, estado_inicial, alfabeto = [], estados = [], estados_de_aceptacion = [], transitions = {}, estado_final = None) -> None:
        
        self.estado_final = estado_final
        self.alfabeto: list = alfabeto #Aceptado como trancisiones (nombre de arista, digamos)
        self.estados: list = estados #Estados (vertices)
        self.estado_inicial = estado_inicial
        self.estados_de_aceptacion: list = [item for item in estados_de_aceptacion if item in self.estados]
        self.transitions: dict = transitions 


    def draw_afd(self):
        afn = graphviz.Digraph(format='pdf')
        afn.graph_attr['rankdir'] = 'LR'
        afn.node('start', style='invis')
        nodos = []
        for state in self.estados:
            if state==self.estado_inicial:
                afn.node(state, shape='diamond', color='red')
                nodos.append((state, "inicial"))
            elif state not in self.estados_de_aceptacion:
                afn.node(state)
                nodos.append((state, "normal"))
            else:
                afn.node(state, shape='doublecircle')
                nodos.append((state, "aceptacion"))

        grafo = []
        for state in self.transitions:
            trans = self.transitions.get(state)
            for symbol in trans:
                if symbol !='ε':
                    next_state = trans.get(symbol)
                    afn.edge(state, next_state, label=symbol)

        afn.render('afd', view=True)


    def simulacion(self, w, show_path = False):
        path = []
        curr_state = self.estado_inicial
        for char in w:
            path.append(curr_state)
            if char not in self.alfabeto:
                print("Cadena contiene caracteres que no pertenecen al alfabeto definido")
                return False
            curr_state = self.transitions.get(curr_state).get(char)
        path.append(curr_state)
        if show_path:
            path = "->".join(path)
            print(path)
        return curr_state in self.estados_de_aceptacion

    def minimize(self):
        table = {}
        for i in range(len(self.estados)):
            for j in range(i + 1, len(self.estados)):
                state_pair = (self.estados[i], self.estados[j])
                if (self.estado_final in state_pair) and (self.estado_final not in self.estados_de_aceptacion):
                    table[state_pair] = False
                else:
                    table[state_pair] = True
        
        while True:
            table_changed = False
            for i in range(len(self.estados)):
                for j in range(i + 1, len(self.estados)):
                    state_pair = (self.estados[i], self.estados[j])
                    if table[state_pair]:
                        for symbol in self.alfabeto:
                            next_state_i = self.transitions[state_pair[0]].get(symbol)
                            next_state_j = self.transitions[state_pair[1]].get(symbol)
                            next_state_pair = (next_state_i, next_state_j)
                            if next_state_pair in table and not table[next_state_pair]:
                                table[state_pair] = False
                                table_changed = True
                                break
                        if table_changed:
                            break
                if table_changed:
                    break
            if not table_changed:
                break
        
        state_groups = {}
        for state in self.estados:
            for state_pair, equivalent in table.items():
                if equivalent and state in state_pair:
                    if state_pair in state_groups:
                        state_groups[state_pair].append(state)
                    else:
                        state_groups[state_pair] = [state]
                    break
        new_states = []
        new_transitions = {}
        new_accept_states = []
        for state_group in state_groups.values():
            new_state_name = ",".join(sorted(state_group))
            new_states.append(new_state_name)
            for symbol in self.alfabeto:
                next_states = set()
                for state in state_group:
                    next_state = self.transitions[state].get(symbol)
                    for state_pair, equivalent in table.items():
                        if equivalent and next_state in state_pair:
                            next_state = ",".join(sorted(state_pair))
                            break
                    next_states.add(next_state)
                new_transitions[new_state_name] = {symbol: ",".join(sorted(next_states))}
            if any(state in self.estados_de_aceptacion for state in state_group):
                new_accept_states.append(new_state_name)
        new_initial_state = ",".join(sorted(state_groups[(self.estado_inicial, None)]))
        
        return AFD(new_initial_state, self.alfabeto, new_states, new_accept_states, new_transitions, None)