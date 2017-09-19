import sublime, sublime_plugin
import os

class CloseTabsCommand(sublime_plugin.WindowCommand):
    def run(self, type = None):
        self.views = self.window.views()
        if type == "left":
            self.close_tabs_left()
        elif type == "group":
            self.close_tabs_group()

    def close_tabs_left(self):
        view_active = self.window.active_view()
        group_active, index_acitve = self.window.get_view_index(view_active)
        views_left = []
        for view in self.views:
            group, index = self.window.get_view_index(view)
            if group == group_active and index < index_acitve:
                views_left.append(view)
        for view in views_left:
            view.close()

    def close_tabs_group(self):
        group_active = self.window.active_group()
        views_group = [view for view in self.views 
            if self.window.get_view_index(view)[0] == group_active]
        for view in views_group:
            view.close()
        self.destroy_group(group_active)

    def destroy_group(self, group):
        pass
        # use set_layout()

