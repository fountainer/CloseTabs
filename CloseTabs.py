import sublime, sublime_plugin
import os

class CloseTabsCommand(sublime_plugin.WindowCommand):
    def close_tabs_left(self, arg, save = None, skip = False):
        if arg == "this":
            view_active = self.window.active_view()
            group_active, index_acitve = self.window.get_view_index(view_active)
            views_left = []
            for view in self.window.views():
                group, index = self.window.get_view_index(view)
                if (group == group_active and index < index_acitve 
                        and not self.is_skip_view(view, skip)):
                    views_left.append(view)
            for view in views_left:
                self.close_view(view, save)
        elif arg == "all":
            # cross groups
            pass
        else:
            sublime.error_message(
                'Undefined argument {} in "{}"'.format(arg, "close_tabs_left"))

    def close_tabs_group(self, arg, save = None, skip = False):
        group_active = self.window.active_group()
        views = self.window.views()
        num_skip = 0
        if arg == "this":
            views_group = []
            for view in views:
                if self.window.get_view_index(view)[0] == group_active:
                    if self.is_skip_view(view, skip):
                        num_skip += 1
                    else:
                        views_group.append(view)
        elif arg == "others":
            views_group = []
            for view in views:
                if self.window.get_view_index(view)[0] != group_active:
                    if self.is_skip_view(view, skip):
                        num_skip += 1
                    else:
                        views_group.append(view)
        else:
            sublime.error_message(
                'Undefined argument {} in "{}"'.format(arg, "close_tabs_group"))
        for view in views_group:
            self.close_view(view, save)
        # require Origami package
        if not num_skip:
            self.window.run_command("destroy_pane", {"direction": "self"})

    def close_tabs_folder(self, arg, save = None, skip = False):
        view_active = self.window.active_view()
        file_name_active = view_active.file_name()
        if file_name_active:
            current_folder = os.path.dirname(file_name_active)
        else:
            sublime.error_message("This file does not exist on disk.")
            return
        num = self.window.num_groups()
        num_views_in_groups = [0] * num
        views = self.window.views()
        for view in views:
            group, _ = self.window.get_view_index(view)
            num_views_in_groups[group] += 1
        views_to_close = []
        for view in views:
            file_name = view.file_name()
            if file_name:
                if (arg == "this" 
                        and os.path.dirname(file_name) == current_folder 
                        and not self.is_skip_view(view, skip)):
                    pass
                elif (arg == "others" 
                        and os.path.dirname(file_name) != current_folder
                        and not self.is_skip_view(view, skip)):
                    pass
                else:
                    continue
                views_to_close.append(view)
                group, _ = self.window.get_view_index(view)
                num_views_in_groups[group] -= 1
            else:
                pass
        if not views_to_close:
            return
        for view in views_to_close:
            self.close_view(view, save)
        i = 0
        while i < len(num_views_in_groups):
            if num_views_in_groups[i] == 0:
                del num_views_in_groups[i]
                self.window.focus_group(i)
                self.window.run_command("destroy_pane", {"direction": "self"})
            else:
                i = i + 1

    def close_view(self, view, save = None):
        if view.is_dirty():
            if save is None:
                pass
            elif save:
                view.run_command("save")
            else:
                view.set_scratch(True)
        view.close()

    def is_skip_view(self, view, skip = False):
        if skip and view.is_dirty():
            return True
        else:
            return False



class CloseTabsLeftCommand(CloseTabsCommand):
    def run(self, arg, save = None, skip = False):
        self.close_tabs_left(arg, save, skip)

class CloseTabsGroupCommand(CloseTabsCommand):
    def run(self, arg, save = None, skip = False):
        self.close_tabs_group(arg, save, skip)

class CloseTabsFolderCommand(CloseTabsCommand):
    def run(self, arg, save = None, skip = False):
        self.close_tabs_folder(arg, save, skip)