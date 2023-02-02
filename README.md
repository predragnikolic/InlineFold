# InlineFold

By default,
InlineFold will fold only string that are preceded with the word "class" or "className".

To chnage the default,
from the command palette open `Preference: Settings` and change the `"inline_fold.rules"` setting:
```
	"inline_fold.rules": [
		{
			"fold_selector": "string.quoted.single, string.quoted.double",
			"preceding_text": "class,className",
		}

		//
		{
			"fold_selector": "meta.function-call.arguments",
		},
		{
			"fold_selector": "source.jsx meta.function.js meta.block.js",
		}
	]
```

- `fold_selector` - The `fold_selector` should be the region that should be folded.
- `preceding_text` - If specified, the region will be folded only if the `preceding_text` is before the `fold_selector`.\nInlineFold will scan max on line before to find the `preceding_text`.