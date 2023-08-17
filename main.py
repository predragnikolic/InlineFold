from typing import List, Optional
import sublime_plugin
import sublime


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

    def schedule(self) -> None:
        cursors = [r for r in self.view.sel()]
        if not cursors:
            return
        if self.last_cursors != cursors:
            self.last_cursors = cursors
            sublime.set_timeout(lambda: self.run_when_stable(cursors), 50)

    def run_when_stable(self, cursors_to_compare: List[sublime.Region]) -> None:
        if self.last_cursors != cursors_to_compare:
            return
        cursors = self.last_cursors
        rules = self.view.settings().get("inline_fold.rules", [])
        for rule in rules:
            fold_regions = self.view.find_by_selector(rule.get('fold_selector'))
            look_region = get_look_region(self.view)
            # reduce the number of regions to improve performance in large files
            fold_regions = list(filter(lambda fold_region: look_region.contains(fold_region), fold_regions))
            for fold_region in fold_regions:
                line = self.view.line(fold_region)
                if fold_region.begin() > line.end():
                    continue
                if fold_region.end() < line.begin():
                    continue
                is_cursor_inside = False
                for cursor in cursors:
                    if line.contains(cursor) or line.intersects(cursor):
                        self.view.unfold(fold_region)
                        is_cursor_inside = True
                if not is_cursor_inside:
                    fold(self.view, fold_region, rule.get('preceding_text'))


class InlineFoldAll(sublime_plugin.TextCommand):
    def run(self, _: sublime.Edit) -> None:
        rules = self.view.settings().get("inline_fold.rules", [])
        for rule in rules:
            fold_regions = self.view.find_by_selector(rule.get('fold_selector'))
            for fold_region in fold_regions:
                fold(self.view, fold_region, rule.get('preceding_text'))


class InlineUnfoldAll(sublime_plugin.TextCommand):
    def run(self, _: sublime.Edit) -> None:
        rules = self.view.settings().get("inline_fold.rules", [])
        for rule in rules:
            fold_regions = self.view.find_by_selector(rule.get('fold_selector'))
            for fold_region in fold_regions:
                self.view.unfold(fold_region)


def fold(view: sublime.View, fold_r: sublime.Region, preceding_text: Optional[str] = None) -> None:
    if view.is_folded(fold_r):
        return
    if preceding_text:
        word_region = view.word(view.find_by_class(fold_r.begin(), False, sublime.PointClassification.WORD_START))
        word = view.substr(word_region)
        if word not in preceding_text.split(','):
            return
        # region Row Tolerance
        # the preceding_text might be a few lines up.
        # by default we will consider 1 row tolerance.
        max_rows_to_tolerate = 1
        word_row, _ = view.rowcol(word_region.begin())
        fold_row, _ = view.rowcol(fold_r.begin())
        if abs(fold_row - word_row) > max_rows_to_tolerate:
            return
        # endregion
    view.fold(fold_r)


def first_selection_region(view: sublime.View) -> Optional[sublime.Region]:
    try:
        return view.sel()[0]
    except IndexError:
        return None

def get_look_region(view: sublime.View) -> sublime.Region:
    visible_region = view.visible_region()
    offset =  10000
    return sublime.Region(visible_region.begin() - offset, visible_region.end() + offset)