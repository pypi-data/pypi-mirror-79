# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tail_recursive']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tail-recursive',
    'version': '1.2.0',
    'description': 'Tail recursion with a simple decorator api.',
    'long_description': '![tests](https://github.com/0scarB/tail-recursive/workflows/Tests/badge.svg)\n\nUse the `tail_recursive` decorator to simply define tail recursive functions.\n\nIf you are encountering **maximum recursion depth errors** or **out-of-memory crashes** tail recursion can be a helpful strategy.\n\n### Example\n\n```python\nimport tail_recursive from tail_recursive\n\n\n# Pick a larger value if n is below your system\'s recursion limit.\nx = 5000\n\n\ndef factorial_without_tail_recursion(n, accumulator=1):\n    if n == 1:\n        return accumulator\n    return factorial_without_tail_recursion(n - 1, n * accumulator)\n\n\ntry:\n    # This will exceed the maximum recursion depth.\n    factorial_without_tail_recursion(x)\nexcept RecursionError:\n    pass\n\n\n@tail_recursive\ndef factorial(n, accumulator=1):\n    if n == 1:\n        return accumulator\n    # It is important that you return the return value of the `tail_call`\n    # method for tail recursion to take effect!\n    return factorial.tail_call(n - 1, n * accumulator)\n\n\n# Implementation with tail recursion succeeds because the function is\n# called sequentially under the hood.\nfactorial(x)\n```\n\nThe `tail_call` method returns an object which stores a function (e.g. `factorial`) and\nits arguments. The function is then lazily evaluated once the object has been returned\nfrom the caller function (in this case also `factorial`). This means that the\nresources in the caller function\'s scope are free to be garbage collected and that its\nframe is popped from the call stack before we push the returned function on.\n\n## Nested Calls\n\nIn the previous example the whole concept of an accumulator my not fit your mental model\nthat well (it doesn\'t for me at least).\nLuckily calls to `tail_call` support nested calls (i.e. another `tail_call` passed as an\nargument).\nTaking this functionality into consideration we can refactor the previous example.\n\n```python\n...\n\n@tail_recursive\ndef mul(a, b):\n    return a * b\n\n@tail_recursive\ndef factorial(n):\n    if n == 1:\n        return n\n    return mul.tail_call(n, factorial.tail_call(n - 1))\n\n...\n```\n\nThis, however, comes a performance cost and can be disabled as follows.\n\n```python\n@tail_recursive(nested_call_mode="do_not_resolve_nested_calls")\ndef factorial(n, accumulator=1):\n    if n == 1:\n        return accumulator\n    return factorial.tail_call(n - 1, n * accumulator)\n```\n\nor\n\n```python\nfrom tail_recursive import tail_recursive, NestedCallMode\n\n...\n\n@tail_recursive(nested_call_mode=NestedCallMode.DO_NOT_RESOLVE_NESTED_CALLS)\ndef factorial(n, accumulator=1):\n    ...\n```\n\nSimilarly, use `nested_call_mode="resolve_nested_calls"` or `nested_call_mode=NestedCallMode.RESOLVE_NESTED_CALLS`\nto explicitly enable this feature.\n\n## Current Limitations\n\n### Return Values\n\nCurrently tail calls that are returned as an item in a tuple or other\ndata structure are not evaluated.\n\nThe following will not evaluate the tail call.\n\n```python\nfrom tail_recursive import tail_recursive\n\n@tail_recursive\ndef func(...):\n    ...\n    return return_val1, func.tail_call(...)\n```\n\nA workaround is to use factory functions.\n\n```python\nfrom tail_recursive import tail_recursive\n\n@tail_recursive\ndef tuple_factory(*args):\n    return tuple(args)\n\n@tail_recursive\ndef func(...):\n    ...\n    return tuple_factory.tail_call(\n        return_val1,\n        func.tail_call(...)\n    )\n```\n\n## Other Packages\n\nCheck out [tco](https://github.com/baruchel/tco) for an alternative api with extra functionality.\n',
    'author': '0scarB',
    'author_email': 'oscarb@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/0scarB/tail-recursive',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
