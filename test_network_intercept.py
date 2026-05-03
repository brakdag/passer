from paser.tools.registry import AVAILABLE_TOOLS

def test_tool_type():
    tool = AVAILABLE_TOOLS.get('network_intercept')
    if tool is None:
        print('Tool network_intercept not found in registry')
        exit(1)
    
    print(f'Tool type: {type(tool)}')
    if hasattr(tool, '__call__'):
        print('Tool is callable')
    else:
        print('Tool is NOT callable')
        exit(1)

if __name__ == '__main__':
    test_tool_type()