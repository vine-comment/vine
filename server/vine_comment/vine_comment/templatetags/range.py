from django.template import Library, Node, NodeList, Variable,\
    TemplateSyntaxError, VariableDoesNotExist

register = Library()

class RangeNode(Node):
    def __init__(self, var_name, start, end, step, nodelist_loop):
        self.var_name = var_name
        self.nodelist_loop = nodelist_loop

        try:
            self.start = int(start)
        except ValueError:
            self.start = Variable(start)

        try:
            self.end = int(end)
        except ValueError:
            self.end = Variable(end)

        try:
            self.step = int(step)
        except ValueError:
            self.step = Variable(step)

    def __iter__(self):
        for node in self.nodelist_loop:
            yield node
   
    def render(self, context):
        nodelist = NodeList()

        context.push()
        try:
            start = self.start.resolve(context)
        except VariableDoesNotExist:
            return ''
        except AttributeError:
            start = self.start

        try:
            end = self.end.resolve(context)
        except VariableDoesNotExist:
            return ''
        except AttributeError:
            end = self.end

        try:
            step = self.step.resolve(context)
        except VariableDoesNotExist:
            return ''
        except AttributeError:
            step = self.step

        for i in xrange(start, end, step):
            context[self.var_name] = i

            for node in self.nodelist_loop:
                nodelist.append(node.render(context))

        context.pop()
        return nodelist.render(context)

@register.tag(name="range")
def do_range(parser, token):
    """
    Work much like forloop with a range.
    Takes both variables and constant integers.
    
    Syntax:
    {% range end as i %}
      {{ i }}
    {% endrange %}
    {% range start:end as i %}
      {{ i }}
    {% endrange %}
    {% range start:step:end as i %}
      {{ i }}
    {% endrange %}

    """

    bits = token.split_contents()
    if len(bits) != 4 or bits[2] != 'as':
        raise TemplateSyntaxError(
            "%r expected format is '[start:][step:]end as name'" % bits[0]
        )
        
    var_name = bits[3]

    rangebits = bits[1].split(':')
    if len(rangebits) == 1:
        start = 0
        end = rangebits[0]
        step = 1
    elif len(rangebits) == 2:
        start = rangebits[0]
        end = rangebits[1]
        step = 1
    elif len(rangebits) == 3:
        start = rangebits[0]
        step = rangebits[1]
        end = rangebits[2]
        
    nodelist = parser.parse(('endrange',))
    parser.delete_first_token()
    return RangeNode(var_name, start, end, step, nodelist)
