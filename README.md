# InlineFold

<!--toc:start-->
- [InlineFold](#inlinefold)
    - [Set Fold Regions Globally](#set-fold-regions-globally)
    - [Set Fold Regions per Syntax](#set-fold-regions-per-syntax)
<!--toc:end-->

By default,
InlineFold will only fold string that are preceded with the word "class" or "className"
and it unfolds when the caret (or selection) touches a line.

![output](https://user-images.githubusercontent.com/22029477/216466685-fe0c97a2-78a0-4462-b6a5-081779cbcdcb.gif)

### Set Fold Regions Globally

From the top menu, select `Preferences > Settings` and change the `"inline_fold.rules"` setting:
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
- `preceding_text` - [Optional] The region will be folded only if the `preceding_text` is found before the `fold_selector`. InlineFold will scan max one line before to find the `preceding_text`. Multiple words can be specified by separating them with a comma `,` (example `"preceding_text": "class,className"`).

### Set Fold Regions per Syntax

If a rule is specific to a particular syntax, for example Python.
Open a python file.
Click `Preferences > Settings - Syntax Specific` and specify the `"inline_fold.rules"`. Those rules will only apply to Python files.

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
