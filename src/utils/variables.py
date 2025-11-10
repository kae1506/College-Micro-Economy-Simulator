# file to define the type for variables. in code i can have the variables be a seperate object
# or i can have the divisions be seperate objects.
# like global_state, actor_state, stuff like that.


# each function call that needs parameters will pass a config dictionary, that 
# will query which parameters it requires.
# code needed: functions to convert parameters to a good state(numpy)
# functions to report the required the parameters
# classes to inherit 
class StateHolder:
    def __init__(self, parameters_init={}):
        self.parameters = {
            "",
            "",
            "",

        }

        self.update_parameters(parameters_init)
        
    def update_parameters(self, parameters_update):
        for key in parameters_update:
            self.parameters[key] = parameters_update[key]

        

class GlobalState(StateHolder):
    def __init__(self, parameters_init_={}):
        super().__init__()
        self.parameters = {
            "","",""
        }

    