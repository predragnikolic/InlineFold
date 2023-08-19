# InlineFold

A Sublime Text plugin that is useful to fold regions into a single line.<br>
It can be useful to hide long strings (for example, TailwindCSS classes).

If the cursor is on the same line where the text was folded because of the `"inline_fold.rules"`,<br> the text will be shown,<br> else the text will be folded.

![output](https://user-images.githubusercontent.com/22029477/216466685-fe0c97a2-78a0-4462-b6a5-081779cbcdcb.gif)

### Set Fold Regions Globally

From the top menu, select `Preferences > Settings` and specify the `"inline_fold.rules"` setting:
```jsonc
// Preferences.sublime-settings
{
    "inline_fold.rules": [
        {
            // Example: <div class="..."></div>
            "fold_selector": "string.quoted.single - punctuation.definition.string, string.quoted.double - punctuation.definition.string",
            "preceding_text": "class,className",
        }
    ]
}
```

- `fold_selector` - [Required] The `fold_selector` is the region that will be folded.
- `preceding_text` - [Optional] The region will be folded only if the `preceding_text` is found before the `fold_selector`. InlineFold will scan max one line before finding the `preceding_text``. Multiple words can be specified by separating them `with a comma`,` (example` `"preceding_text": "class,className"`).

### Set Fold Regions per Syntax

If a rule is specific to a particular syntax, for example, Python.
Open a Python file.
Click `Preferences > Settings - Syntax Specific` and specify the `"inline_fold.rules"`. Those rules will only apply to Python files:


```jsonc
// Python.sublime-settings
{
    "inline_fold.rules": [
        {
            // Example: view.run_command(...)
            // The `- punctuation.section.arguments.begin` will not fold the open bracket
            // The `- punctuation.section.arguments.end` will not fold the close bracket
            "fold_selector": "meta.function-call.arguments.python - punctuation.section.arguments.begin - punctuation.section.arguments.end",
        }
    ]
}
```

### Recipes

Here is a list of recipes:

```jsonc
{
    "inline_fold.rules": [
        // Fold TailwindCSS class names
        // Example: <div class="..."></div>
        {
            "fold_selector": "string.quoted.single - punctuation.definition.string, string.quoted.double - punctuation.definition.string",
            "preceding_text": "class,className",
        },

        // [Python] Fold docstring except for the first line of the docs string.
        // class Person:
        //     """
        //     Some really long docs string. ..."""
        {
            "fold_selector": "comment.block.documentation.python - punctuation.definition.comment",
        }
    ]
}
```





