# InlineFold

By default,
InlineFold will only fold string that are preceded with the word "class" or "className"
and it unfolds when the caret (or selection) touches a line.

![output](https://user-images.githubusercontent.com/22029477/216466685-fe0c97a2-78a0-4462-b6a5-081779cbcdcb.gif)

### Change Fold Regions

From the command palette open `Preference: Settings` and change the `"inline_fold.rules"` setting:
```jsonc
// Preferences.sublime-settings
{
    "inline_fold.rules": [
        {
            // Example: <div class="..."></div>
            "fold_selector": "string.quoted.single, string.quoted.double",
            "preceding_text": "class,className",
        }
    ]
}
```

- `fold_selector` - The `fold_selector` should be the region that should be folded.
- `preceding_text` - If specified, the region will be folded only if the `preceding_text` is before the `fold_selector`. InlineFold will scan max on line before to find the `preceding_text`.

Other examples:
```jsonc
{
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
}
```
