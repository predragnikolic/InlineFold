from typing import List, Optional
import sublime_plugin
import sublime

string_scope = 'string.quoted.single, string.quoted.double'
preceding_text = ['class', 'className']

def plugin_loaded():
    views = sublime.active_window().views()
    for v in views:
        v.run_command("inline_fold_all")


class InlineFoldListener(sublime_plugin.ViewEventListener):
    def on_load(self) -> None:
        self.view.run_command('inline_fold_all')

    def on_selection_modified(self) -> None:
        # validation
        r = first_selection_region(self.view)
        if r is None:
            return

        cursors = [r for r in self.view.sel()]

        strings = find_strings(self.view)
        for string in strings:
            fold_region = get_fold_region(self.view, string)
            line = self.view.line(string)
            if string.begin() > line.end():
                continue
            if string.end() < line.begin():
                continue
            is_cursor_inside = False
            for cursor in cursors:
                if line.contains(cursor) or line.intersects(cursor):
                    self.view.unfold(string)
                    is_cursor_inside = True
            if not is_cursor_inside:
                fold(self.view, fold_region)


def get_fold_region(view: sublime.View, string_region: sublime.Region):
    start = view.find(r"""("|')""", string_region.begin())
    end = view.find(r"""("|')""", string_region.end() - 1)
    return sublime.Region(start.begin() + 1, end.end() - 1)


def fold(view: sublime.View, fold_r: sublime.Region):
    word = view.substr(view.word(view.find_by_class(fold_r.begin(), False, sublime.PointClassification.WORD_START)))
    if not view.is_folded(fold_r) and word in preceding_text:
        view.fold(fold_r)


class InlineFoldAll(sublime_plugin.TextCommand):
    def run(self, _: sublime.Edit) -> None:
        strings = find_strings(self.view)
        for string in strings:
            fold_region = get_fold_region(self.view, string)
            fold(self.view, fold_region)


class InlineUnfoldAll(sublime_plugin.TextCommand):
    def run(self, _: sublime.Edit) -> None:
        regions = find_strings(self.view)
        for r in regions:
            self.view.unfold(r)

def first_selection_region(view: sublime.View) -> Optional[sublime.Region]:
    try:
        return view.sel()[0]
    except IndexError:
        return None

def find_strings(view: sublime.View) -> List[sublime.Region]:
    return view.find_by_selector(string_scope)