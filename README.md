# InlineFold

By default,
InlineFold will fold only string that are preceded with the word "class" or "className".

To chnage the default,
from the command palette open `Preference: Settings` and change the `"inline_fold.rules"` setting:
```
	"inline_fold.rules": [
		{
			// Example: <div class="..."></div>
			"fold_selector": "string.quoted.single, string.quoted.double",
			"preceding_text": "class,className",
		}
	]
```

- `fold_selector` - The `fold_selector` should be the region that should be folded.
- `preceding_text` - If specified, the region will be folded only if the `preceding_text` is before the `fold_selector`.\nInlineFold will scan max on line before to find the `preceding_text`.

Other examples:
```
	"inline_fold.rules": [
		{
			// Example: <div class="..."></div>
			"fold_selector": "string.quoted.single, string.quoted.double",
			"preceding_text": "class,className",
		},
		{
			// Example (only Python): v.run_command(...)
			"fold_selector": "meta.function-call.arguments.python",
		},
		{
			// Example (only JavaScript): foo(a, b) {...}
			"fold_selector": "source.js meta.function.js meta.block.js",
		}
	]
```