from pinject import new_object_graph, BindingSpec

specs = []
boot = False
graph = None
classes = []
class_name_arg_name_mapping: dict = {}
instance_arg_name_mapping: dict = {}

"""
inject an instance and inject an object are difference.
Only support for inject class. (to_class binding)
To inject an instance, declaring a custom spec with to_instance binding and registering it.
"""


class ExplicitClassBindingSpec(BindingSpec):
    def configure(self, bind):
        for class_name, arg_name in class_name_arg_name_mapping.items():
            bind(arg_name, to_class=class_name)


# Use this function at file-level to register a class as a Dependency
def register_class(target, arg_name=None):
    if arg_name:
        class_name_arg_name_mapping.update({arg_name: target})
        return None
    classes.append(target)


def register_spec(spec):
    global specs
    specs.append(spec)


def __load_graph(objects):
    global graph, boot, specs
    specs.append(ExplicitClassBindingSpec())
    graph = new_object_graph(modules=None, classes=objects, binding_specs=specs)
    boot = True


# Only use inject inside target class for avoiding un-completed bootstrapping
def inject(target):
    if not boot:
        __load_graph(classes)
    return graph.provide(target)
