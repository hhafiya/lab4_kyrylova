from graphviz import Digraph

dot = Digraph()

states = ["wake_up", "eat", "fight", "gather", "build", "sleep", "explore", "death", "dead"]
start_state = "wake_up"
end_states = ["sleep", "dead"]
transitions = [
    ("wake_up", "eat", "time\n8.30am"),
    ("wake_up", "gather", "time\n8.30am"),
    ("gather", "eat", "time\n12.30pm"),
    ("gather", "fight", "time\n12.30pm"),
    ("gather", "build", "time\n12.30pm\nno house"),
    ("build", "explore", "time\n18pm"),
    ("explore", "fight", "time\n20pm\nmob attack"),
    ("explore", "eat", "time\n20pm"),
    ("explore", "build", "time\n20pm"),
    ("build", "eat", "time\n18pm"),
    ("eat", "build", "time\n14.30pm"),
    ("fight", "death", "health\n0"),
    ("fight", "gather", "health\n>0"),
    ("death", "dead", "life count\n0"),
    ("death", "wake_up", "life count\n>0"),
    ("build", "sleep", "time\n22pm"),
    ("gather", "sleep", "time\n22pm"),
    ("eat", "sleep", "time\n22pm"),
    ("explore", "sleep", "time\n22pm"),
    ("wake_up", "eat", "time\n14pm"),
]


dot.node('start', style='invisible')

for state in states:
    if state in end_states:
        dot.node(state, style='filled', fillcolor='grey', shape='doublecircle')
    else:
        dot.node(state)

dot.edge('start', start_state)

for i, transition in enumerate(transitions):
    dot.edge(transition[0], transition[1], label=transition[2])

dot.render('state_machine.gv', view=True)