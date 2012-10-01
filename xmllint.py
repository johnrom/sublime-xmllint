import os
import re
import sublime
import sublime_plugin
import thread
import subprocess
import functools
import time
#import xmlparse
import sys

RESULT_VIEW_NAME = 'xmllint_result_view'
SETTINGS_FILE = "sublime-xmllint.sublime-settings"


class XmlDocCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.errors = ''
        s = sublime.load_settings(SETTINGS_FILE)

        self.xml_doc_types = s.get('xml_doctypes', [])
        self.doc = self.view.substr(sublime.Region(0, self.view.size()))
        schema = self.check_schema()

        sublime.active_window().run_command('xml_lint', {'schema': schema, 'errors': self.errors})

    def check_schema(self):
        schema_index = re.search('xmlns:xsi=', self.doc)
        if schema_index:
            line = self.view.line(schema_index.start())
            schema_line = self.view.substr(line)
            find_schema = re.search('SchemaLocation="([^"]*)', schema_line)
            if find_schema:
                schema = find_schema.group(1)
            else:
                schema = 'Invalid'
                self.view.run_command("goto_line", {"line": line})
                self.errors += schema_line + '\n'
        else:
            schema = None

        return schema


class XmlLintCommand(sublime_plugin.WindowCommand):
    exec_set = 0

    def run(self, schema, errors):
        s = sublime.load_settings(SETTINGS_FILE)

        file_path = self.window.active_view().file_name()
        file_name = os.path.basename(file_path)

        self.schema = schema
        self.buffered_data = ''
        self.file_path = file_path
        self.file_name = file_name
        self.is_running = True
        self.tests_panel_showed = False
        self.ignored_error_count = 0
        self.lint_errors = errors

        """self.ignore_errors = s.get('ignore_errors', [])"""
        self.xml_doc_types = s.get('xml_doctypes', [])
        self.args = s.get('args', [])
        if schema:
            if schema == 'Invalid':
                self.lint_errors = 'Invalid schema, check schema location tag\n'
            else:
                self.args.append("--schema " + schema)
        args = ' '.join(self.args)
        self.init_tests_panel()
        self.lint_errors += args
        self.return_code = None

        if len(s.get('xmllint_exec', '')) > 0:
            lint_exec = s.get('xmllint_exec')
        else:
            lint_exec = 'xmllint.exe'

        # if self.debug:
        #   print "DEBUG: " + str(cmd + '' + lint_exec)

        exec_file = self.find_exec(lint_exec)

        if exec_file == None:
            self.lint_errors += 'Could not find executable for "XMLLint." Google "LibXML2". Also, I work! \n'
        else:
            self.lint_finder(self, exec_file, args)

    def find_exec(self, lint_exec):
        def is_exe(path_unescaped):
            path = path_unescaped.replace('\\', '\\\\')

            return os.path.isfile(path) and os.access(path, os.X_OK)

        exec_path, name = os.path.split(lint_exec)
        if exec_path:
            if is_exe(lint_exec):
                return lint_exec
        else:
            if self.exec_set == 0:
                sys.path.append(''.join([sublime.packages_path(), '\\sublime-xmllint\\libxml']))
            for path in sys.path:
                exe_file = os.path.join(path, lint_exec)
                if is_exe(exe_file):
                    return ''.join(['"', exe_file, '"'])
        return None

    def lint_finder(self, listener, exec_file, args):
        file_path = self.file_path
        self.listener = listener
        cmd = exec_file + ' ' + args + ' ' + file_path
        print cmd
        self.valid = False
        self.proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if self.proc.stdout:
            thread.start_new_thread(self.read_stdout, ())

        if self.proc.stderr:
            thread.start_new_thread(self.read_stderr, ())

        thread.start_new_thread(self.poll, ())

    def poll(self):
        while True:
            if self.proc.poll() != None:
                sublime.set_timeout(functools.partial(self.listener.proc_terminated, self.proc), 0)
                break
            time.sleep(0.1)

    def read_stdout(self):
        while True:
            data = os.read(self.proc.stdout.fileno(), 2 ** 15)
            self.msgdata = data
            if data != "":
                sublime.set_timeout(functools.partial(self.listener.show_errors, self.proc, data), 0)
            else:
                self.proc.stdout.close()
                self.listener.is_running = False
                break

    def read_stderr(self):
        while True:
            data = os.read(self.proc.stderr.fileno(), 2 ** 15)
            if data != "":
                validates = re.search(self.file_name + ' validates', data)
                if validates:
                    valid = 1
                else:
                    valid = 0
                sublime.set_timeout(functools.partial(self.listener.show_errors, self.proc, data, valid), 0)
            else:
                self.proc.stderr.close()
                self.listener.is_running = False
                break

    def proc_terminated(self, proc):
        self.return_code = proc.returncode
        if proc.returncode == 0:
            msg = self.file_name + ' lint free!\n'
        elif proc.returncode == 4 and self.schema:
            if self.valid == 1:
                msg = self.file_name + ' lint free!\n'
            else:
                msg = ''
        else:
            msg = ''

        self.show_errors(proc, msg, True)

    def show_errors(self, proc, data, end=False):
        return_codes = {
            0: 'No error',
            1: 'Unclassified',
            2: 'Error in DTD',
            3: 'Validation error',
            4: 'Validation error',
            5: 'Error in schema compilation',
            6: 'Error writing output',
            7: 'Error in pattern (generated when [--pattern] option is used)',
            8: 'Error in Reader registration (generated when [--chkregister] option is used)',
            9: 'Out of memory error'
        }
        if end == 0:
            self.parse_errors(data)
        elif end == False:
            self.write_to_panel(data)
        elif end == True:
            if self.return_code:
                returncode = str(self.return_code) + ': ' + return_codes[self.return_code]
                self.write_to_panel(returncode)
            else:
                lintfree = str(data) + '\n'
                self.write_to_panel(lintfree)
            ignored = 'xmllint: ignored ' + str(self.ignored_error_count) + ' errors.'
            self.write_to_panel(ignored)

    def parse_errors(self, data):
        errors = None
        replaced_line = None
        lines = re.split("\n", data)
        for line in lines:
            reggie = re.search(r'file:///C:/[^:]*:\d*:\s((?:([^:]*):?)*)', line)
            if reggie and reggie != '':
                replaced_line = []
                for group in reggie.groups():
                    if group != '':
                        replaced_line.append(re.sub(r'\s*:\s*', '-', group))
                if replaced_line:
                    if errors == None:
                        errors = []
                    errors.append(replaced_line)
        if errors:
            formatted_errors = self.format_errors(errors)
            self.write_to_panel(formatted_errors)

    def write_to_panel(self, data=False):
        if data != False:
            output = str(data) + '\n'
        else:
            output = self.response + '\n'
        if output:
            self.show_tests_panel()
            self.output_view.set_read_only(False)
            edit = self.output_view.begin_edit()
            self.output_view.insert(edit, self.output_view.size(), output)
            self.output_view.end_edit(edit)
            self.output_view.set_read_only(True)

    def format_errors(self, errors):
        for error in errors:
            error_msg = '-'.join(error)
        return error_msg

    def init_tests_panel(self):
        if not hasattr(self, 'output_view'):
            self.output_view = self.window.get_output_panel(RESULT_VIEW_NAME)
            self.output_view.set_name(RESULT_VIEW_NAME)
        self.clear_test_view()
        self.output_view.settings().set("file_path", self.file_path)

    def show_tests_panel(self):
        if self.tests_panel_showed:
            return
        self.window.run_command("show_panel", {"panel": "output." + RESULT_VIEW_NAME})
        self.tests_panel_showed = True

    def clear_test_view(self):
        self.output_view.set_read_only(False)
        edit = self.output_view.begin_edit()
        self.output_view.erase(edit, sublime.Region(0, self.output_view.size()))
        self.output_view.end_edit(edit)
        self.output_view.set_read_only(True)


class XmlLintEventListener(sublime_plugin.EventListener):
    # jslint event
    disabled = False

    def __init__(self):
        self.previous_resion = None
        self.file_view = None

    def on_post_save(self, view):
        s = sublime.load_settings(SETTINGS_FILE)
        if s.get('run_on_save', False) == False:
            return

        if view.file_name().endswith('.xml') == False:
            return

        self.file_view = view
        
        # run xmllint.
        sublime.active_window().run_command("xml_doc")

    def on_deactivated(self, view):
        if view.name() != RESULT_VIEW_NAME:
            return
        self.previous_resion = None

        if self.file_view:
            self.file_view.erase_regions(RESULT_VIEW_NAME)
