class HTML:
    def __init__(self, output=None):
        self.output = output
        self.tag = 'html'
        self.children = []
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        if self.output == None:
            print(f'<{self.tag}>')
            for child in self.children:
                print(str(child))
            print(f'</{self.tag}>')
        else:
            with open(self.output, "w") as f:
                f.write(str(self))
    
    def __iadd__(self, other):
        self.children.append(other)
        return self
    
    def __str__(self):
        line = '<html>\n'
        if self.children:
            for child in self.children:
                line += str(child)
        line += '</html>'
        return line

class TopLevelTag:
    def __init__(self, tag):
        self.tag = tag
        self.children = []
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        pass
    def __iadd__(self, other):
        self.children.append(other)
        return self
    def __str__(self):
        line = f'<{self.tag}>'
        if self.children:
            for child in self.children:
                line += str(child)
        line += f'\n</{self.tag}>\n'
        return line

class Tag:
    def __init__(self, tag, toplevel = False, is_single = False, **kwargs):
        self.tag = tag
        self.toplevel = toplevel
        self.is_single = is_single
        self.text = ''
        self.attributes = {}
        self.children = []
        for attr, value in kwargs.items():
            if attr == "klass":
                self.attributes[attr] = ' '.join(value)
            else:
                self.attributes[attr] = value
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        pass
    def __iadd__(self, other):
        self.children.append(other)
        return self
    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():            
            attrs.append(f"{attribute} = '{value}'")
        attrs = ' '.join(attrs)
        if self.attributes:
            line = f'\n<{self.tag} {attrs}>'
        elif self.is_single and len(self.attributes) == 0:
            line = f'<{self.tag}>'
        else:
            line = f'\n<{self.tag}>'
        if self.children:
            for child in self.children:
                line += str(child)
        if not self.is_single:
            line += f'{self.text}</{self.tag}>'
        else:
            line += '\n'
        return line