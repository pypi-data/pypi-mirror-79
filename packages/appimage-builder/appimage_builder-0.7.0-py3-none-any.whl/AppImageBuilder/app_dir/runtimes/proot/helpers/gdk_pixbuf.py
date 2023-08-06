#  Copyright  2020 Alexis Lopez Zubieta
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
import os
import subprocess

from AppImageBuilder.app_dir.runtimes.classic.helpers.base_helper import BaseHelper


class GdkPixbuf(BaseHelper):

    def configure(self, app_run):
        path = self._get_gdk_pixbuf_loaders_path()
        if path:
            bin_path = self._get_gdk_pixbuf_query_loaders_path()
            if bin_path:
                subprocess_env = os.environ.copy()
                subprocess_env['GDK_PIXBUF_MODULEDIR'] = '/%s' % path
                subprocess_env['GDK_PIXBUF_MODULE_FILE'] = '/%s/loaders.cache' % os.path.dirname(path)

                subprocess.run(
                    ['proot', '-R', self.app_dir, '/%s' % bin_path, '--update-cache'],
                    cwd=self.app_dir, env=subprocess_env)

    def _get_gdk_pixbuf_loaders_path(self):
        return self._get_glob_relative_sub_dir_path('*/usr/*/gdk-pixbuf-2.0/*/loaders/*')

    def _get_gdk_pixbuf_query_loaders_path(self):
        return self._get_relative_file_path('gdk-pixbuf-query-loaders')
