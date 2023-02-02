from typing import List, Optional
import sublime_plugin
import sublime

string_scope = 'string.quoted.single, string.quoted.double, meta.function-call.arguments'
# preceding_text = ['class', 'className']
preceding_text = []

def plugin_loaded():
    views = sublime.active_window().views()
    for v in views:
        v.run_command("inline_fold_all")


def plugin_unloaded():
    views = sublime.active_window().views()
    for v in views:
        v.run_command("inline_unfold_all")


class InlineFoldListener(sublime_plugin.ViewEventListener):
    def __init__(self, view: sublime.View) -> None:
        super().__init__(view)
        self.last_cursors = []

    def on_load(self) -> None:
        self.view.run_command('inline_fold_all')

    def on_selection_modified(self) -> None:
        self.schedule()

    def schedule(self):
        cursors = self.get_cursors()
        if not cursors:
            return
        if self.last_cursors != cursors:
            self.last_cursors = cursors
            sublime.set_timeout(lambda: self.run_when_stable(cursors), 50)

    def run_when_stable(self, cursors_to_compare: List[sublime.Region]):
        if self.last_cursors != cursors_to_compare:
            return
        cursors = cursors_to_compare
        strings = find_strings(self.view)
        for string in strings:
            fold_region = get_fold_region(string)
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

    def get_cursors(self) -> List[sublime.Region]:
        return [r for r in self.view.sel()]

def get_fold_region(string_region: sublime.Region) -> sublime.Region:
    return sublime.Region(string_region.begin() + 1, string_region.end() - 1)


def fold(view: sublime.View, fold_r: sublime.Region) -> None:
    if view.is_folded(fold_r):
        return
    if preceding_text:
        word = view.substr(view.word(view.find_by_class(fold_r.begin(), False, sublime.PointClassification.WORD_START)))
        if word not in preceding_text:
            return
    view.fold(fold_r)


class InlineFoldAll(sublime_plugin.TextCommand):
    def run(self, _: sublime.Edit) -> None:
        strings = find_strings(self.view)
        for string in strings:
            fold_region = get_fold_region(string)
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