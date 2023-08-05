# Convert Case
Cross-language library to convert case with permissive inputs.

## Language supported
The library is available in:
- [js](#code-example-javascript)
- [python](#code-example-python)

## Code examples 
### Code example: JavaScript 

```js
import { camelCase } from "../src/index";

camelCase("helloGreat world");  // helloGreatWorld
camelCase("__hello Great--world");  // helloGreatWorld
```

### Code example: Python
```python
from case_convert import camel_case

camel_case("helloGreat world")  # helloGreatWorld
camel_case("__hello Great--world")  # helloGreatWorld
```

## Cases supported
The library can convert to the following cases:
- camel
- kebab
- pascal
- snake
- upper

## Issues/Bug report or improvement ideas
https://gitlab.com/olive007/case-convert/-/issues

## License
GNU Lesser General Public License v3 or later (LGPLv3+)
