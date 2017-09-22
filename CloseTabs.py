import sublime, sublime_plugin
import os

class CloseTabsCommand(sublime_plugin.WindowCommand):
    def close_tabs_left(self, arg):
        if arg == "this":
            view_active = self.window.active_view()
            group_active, index_acitve = self.window.get_view_index(view_active)
            views_left = []
            for view in self.window.views():
                group, index = self.window.get_view_index(view)
                if group == group_active and index < index_acitve:
                    views_left.append(view)
            for view in views_left:
                view.close()
        elif arg == "all":
            # cross groups
            pass
        else:
            sublime.error_message(
                'Undefined argument {} in "{}"'.format(arg, "close_tabs_left"))

    def close_tabs_group(self, arg):
        group_active = self.window.active_group()
        views = self.window.views()
        if arg == "this":
            views_group = [view for view in views 
                if self.window.get_view_index(view)[0] == group_active]
        elif arg == "others":
            views_group = [view for view in views 
                if self.window.get_view_index(view)[0] != group_active]
        else:
            sublime.error_message(
                'Undefined argument {} in "{}"'.format(arg, "close_tabs_group"))
        for view in views_group:
            view.close()
        # require Origami package
        self.window.run_command("destroy_pane", {"direction": "self"})

    def close_tabs_folder(self, arg):
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
                if arg == "this" and os.path.dirname(file_name) == current_folder:
                    pass
                elif arg == "others" and os.path.dirname(file_name) != current_folder:
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
            view.close()
        i = 0
        while i < len(num_views_in_groups):
            if num_views_in_groups[i] == 0:
                del num_views_in_groups[i]
                self.window.focus_group(i)
                self.window.run_command("destroy_pane", {"direction": "self"})
            else:
                i = i + 1

class CloseTabsLeftCommand(CloseTabsCommand):
    def run(self, arg):
        self.close_tabs_left(arg)

class CloseTabsGroupCommand(CloseTabsCommand):
    def run(self, arg):
        self.close_tabs_group(arg)

class CloseTabsFolderCommand(CloseTabsCommand):
    def run(self, arg):
        self.close_tabs_folder(arg)