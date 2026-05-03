from paser.tools.registry import AVAILABLE_TOOLS
import types

print('Checking AVAILABLE_TOOLS...')
print(f'Total tools: {len(AVAILABLE_TOOLS)}')

for name, func in AVAILABLE_TOOLS.items():
    if name in ['playwright_execute', 'network_intercept', 'proxy_rotate']:
        print(f'{name}: {type(func)}')

print('Done.')
