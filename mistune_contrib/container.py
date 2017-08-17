#coding: utf8
import re
from mistune import BlockLexer, Renderer, Markdown

class ContainerBlockMixin(object):
    def enable_container(self):
        self.rules.block_container = re.compile('^::: ([^\n]*?)\n(.*):::', re.DOTALL)
        self.default_rules.insert(0, 'block_container')

    def parse_block_container(self, m):
        self.tokens.append({
            'type': 'block_container',
            'name': m.groups(0)[0],
            'text': m.groups(0)[1]
        })

class ContainerRendererMixin(object):
    def output_block_container(self, name, text):
        return '<div class="{}">{}</div>'.format(name, text)

class ContainerBlockLexer(ContainerBlockMixin, BlockLexer):
    def __init__(self, *args, **kwargs):
        super(ContainerBlockLexer, self).__init__(*args, **kwargs)
        self.enable_container()

class ContainerRenderer(ContainerRendererMixin, Renderer):
    def __init__(self, *args, **kwargs):
        super(ContainerRenderer, self).__init__(*args, **kwargs)

class MarkdownContainer(Markdown):
    def __init__(self, *args, **kwargs):
        kwargs['renderer'] = ContainerRenderer()
        kwargs['block'] = ContainerBlockLexer
        super(MarkdownContainer, self).__init__(*args, **kwargs)

    def output_block_container(self):
       return self.renderer.output_block_container(self.token['name'],
                self.output(self.token['text']))

def markdown(text, escape=True, **kwargs):
    return MarkdownContainer(escape=escape, **kwargs)(text)
