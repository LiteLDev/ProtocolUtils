from bs4 import BeautifulSoup

raw = open('enums.html').read()
raw.replace('<uint32_t>', '&lt;uint32_t&gt;')

soup = BeautifulSoup(raw, features='lxml')

result = str()
count = 0

for node in soup.body.table.children:
    if node.th: # head
        continue
    reading = 0
    for element in node.children:
        if element.name == None:
            continue
        if reading == 0:
            count += 1
            result += 'enum class %s {\n' % element.string
        elif reading == 1:
            for content in element.children:
                match content.name:
                    case 'br':
                        result += ',\n'
                    case None:
                        result += '    %s' % content.string
                    case _:
                        raise Exception('Unexpected elements! (%s)' % content.name)
        else:
            raise Exception('Unexpected elements!')
        reading += 1
    if reading > 0:
        result += '\n};\n\n'

with open('enums.h', 'w') as file:
    file.write(result.removesuffix('\n'))

print('done, parsed %d type(s).' % count)