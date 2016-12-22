from mako.template import Template
import json

t_str = '''
/**************************************************
* Reflection for ${T}
* auto generated by reflection system
**************************************************/

//#include <cereal/cereal.hpp>
//#include <cereal/types/base_class.hpp>
//#include <cereal/types/polymorphic.hpp>
#include "../ReflectClass.hpp"
#include "../${Header}"

namespace ${Namespace}
{
    
}
'''
t = Template(t_str)

#register_teamplate
componentInheritance_template_str = '''
static std::map<std::string, std::string> s_componentInheritance = {
    ${pairs}
};
'''

classname_template_str = '''

'''

def GenClassFunctions(class_info):
    def IsComponent(name):
        #print(name)
        if name == "Component":
            return True
        if 'parent' not in class_info[name]:
            return False
        return IsComponent(class_info[name]['parent'])

    pairs = []
    for key in class_info.keys():
        if "Component" == key:
             pairs.append((key, ''))
        elif IsComponent(key):
            pairs.append((key, class_info[key]['parent']))
    pairs = ['{{"{0}", "{1}"}},'.format(x, y) for (x, y) in pairs]
    #print(pairs)
    print(Template(componentInheritance_template_str).render(pairs='\n\t'.join(pairs)))

if __name__ == "__main__":
    with open('temp/class.json') as f:
        class_info = json.loads(f.read())
    GenClassFunctions(class_info)
