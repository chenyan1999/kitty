#!/usr/bin/env python3
"""
Test cases for commit c4c62c1505c48f90d75554f02030b76414637f8a
Testing changes related to --keep-focus flag and active history management

Uses AST parsing to test behavior without regex pattern matching.
Trivial issues like missing Optional type annotations are allowed.
"""

import sys
import os
import ast

# Add the parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def read_file(filepath):
    """Read file content"""
    with open(filepath, 'r') as f:
        return f.read()


def get_function_signature(source_code, class_name, method_name):
    """Extract function signature from source code using AST"""
    tree = ast.parse(source_code)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == method_name:
                    # Extract parameter names and defaults
                    params = {}
                    defaults_offset = len(item.args.args) - len(item.args.defaults)

                    for i, arg in enumerate(item.args.args):
                        param_name = arg.arg
                        if i >= defaults_offset:
                            default_idx = i - defaults_offset
                            default = item.args.defaults[default_idx]
                            params[param_name] = default
                        else:
                            params[param_name] = None

                    return params
    return None


def function_calls_method_with_param(source_code, class_name, method_name, called_method, param_name):
    """Check if a method calls another method with a specific parameter"""
    tree = ast.parse(source_code)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == method_name:
                    # Look for calls to the specified method with the parameter
                    for child in ast.walk(item):
                        if isinstance(child, ast.Call):
                            # Check if this is a call to the target method
                            call_name = None
                            if isinstance(child.func, ast.Attribute):
                                call_name = child.func.attr
                            elif isinstance(child.func, ast.Name):
                                call_name = child.func.id

                            if call_name == called_method:
                                # Check if param_name is in keyword arguments
                                for keyword in child.keywords:
                                    if keyword.arg == param_name:
                                        return True
    return False


def test_1_set_active_window_signature():
    """Test that Boss.set_active_window method has for_keep_focus parameter"""
    try:
        content = read_file('kitty/boss.py')
        params = get_function_signature(content, 'Boss', 'set_active_window')

        if params is None:
            print("Test 1 failed when checking Boss.set_active_window method: method not found")
            return

        if 'for_keep_focus' not in params:
            print("Test 1 failed when checking Boss.set_active_window signature: for_keep_focus parameter missing")
            return

        # Check default value is False (allowing for trivial type annotation issues)
        default = params['for_keep_focus']
        if isinstance(default, ast.Constant):
            if default.value != False:
                print(f"Test 1 failed when checking default value: expected False, got {default.value}")
                return

        print("Test 1 passed.")
    except Exception as e:
        print(f"Test 1 failed when reading boss.py: {e}")


def test_2_set_active_tab_call_with_for_keep_focus():
    """Test that Boss.set_active_window calls tm.set_active_tab with for_keep_focus parameter"""
    try:
        content = read_file('kitty/boss.py')
        result = function_calls_method_with_param(content, 'Boss', 'set_active_window', 'set_active_tab', 'for_keep_focus')

        if not result:
            print("Test 2 failed when checking tm.set_active_tab call: for_keep_focus parameter not found in call")
            return

        print("Test 2 passed.")
    except Exception as e:
        print(f"Test 2 failed when reading boss.py: {e}")


def test_3_tab_set_active_window_call():
    """Test that Boss.set_active_window calls tab.set_active_window with for_keep_focus parameter"""
    try:
        content = read_file('kitty/boss.py')
        result = function_calls_method_with_param(content, 'Boss', 'set_active_window', 'set_active_window', 'for_keep_focus')

        if not result:
            print("Test 3 failed when checking tab.set_active_window call: for_keep_focus parameter not found in call")
            return

        print("Test 3 passed.")
    except Exception as e:
        print(f"Test 3 failed when reading boss.py: {e}")


def test_4_launch_keep_focus_call():
    """Test that launch.py calls boss.set_active_window with for_keep_focus=True"""
    try:
        content = read_file('kitty/launch.py')
        tree = ast.parse(content)

        found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute) and node.func.attr == 'set_active_window':
                    for keyword in node.keywords:
                        if keyword.arg == 'for_keep_focus':
                            if isinstance(keyword.value, ast.Constant) and keyword.value.value == True:
                                found = True

        if not found:
            print("Test 4 failed when checking launch.py: for_keep_focus=True not found in boss.set_active_window call")
            return

        print("Test 4 passed.")
    except Exception as e:
        print(f"Test 4 failed when reading launch.py: {e}")


def test_5_tab_set_active_window_signature():
    """Test that Tab.set_active_window method has for_keep_focus parameter"""
    try:
        content = read_file('kitty/tabs.py')
        params = get_function_signature(content, 'Tab', 'set_active_window')

        if params is None:
            print("Test 5 failed when checking Tab.set_active_window method: method not found")
            return

        if 'for_keep_focus' not in params:
            print("Test 5 failed when checking Tab.set_active_window signature: for_keep_focus parameter missing")
            return

        # Check default value is None (allowing for trivial type annotation issues)
        default = params['for_keep_focus']
        if isinstance(default, ast.Constant):
            if default.value is not None:
                print(f"Test 5 failed when checking default value: expected None, got {default.value}")
                return

        print("Test 5 passed.")
    except Exception as e:
        print(f"Test 5 failed when reading tabs.py: {e}")


def test_6_windows_set_active_window_group_for_call():
    """Test that Tab.set_active_window calls windows.set_active_window_group_for with for_keep_focus"""
    try:
        content = read_file('kitty/tabs.py')
        result = function_calls_method_with_param(content, 'Tab', 'set_active_window', 'set_active_window_group_for', 'for_keep_focus')

        if not result:
            print("Test 6 failed when checking windows.set_active_window_group_for call: for_keep_focus parameter not found")
            return

        print("Test 6 passed.")
    except Exception as e:
        print(f"Test 6 failed when reading tabs.py: {e}")


def test_7_tab_manager_set_active_tab_signature():
    """Test that TabManager.set_active_tab method has for_keep_focus parameter"""
    try:
        content = read_file('kitty/tabs.py')
        params = get_function_signature(content, 'TabManager', 'set_active_tab')

        if params is None:
            print("Test 7 failed when checking TabManager.set_active_tab method: method not found")
            return

        if 'for_keep_focus' not in params:
            print("Test 7 failed when checking TabManager.set_active_tab signature: for_keep_focus parameter missing")
            return

        # Check default value is None (allowing for trivial type annotation issues)
        default = params['for_keep_focus']
        if isinstance(default, ast.Constant):
            if default.value is not None:
                print(f"Test 7 failed when checking default value: expected None, got {default.value}")
                return

        print("Test 7 passed.")
    except Exception as e:
        print(f"Test 7 failed when reading tabs.py: {e}")


def test_8_active_tab_history_logic():
    """Test that TabManager.set_active_tab contains active tab history manipulation logic"""
    try:
        content = read_file('kitty/tabs.py')
        tree = ast.parse(content)

        method_found = False
        has_history_check = False

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'TabManager':
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == 'set_active_tab':
                        method_found = True
                        method_source = ast.get_source_segment(content, item)

                        if method_source:
                            has_history_check = (
                                'for_keep_focus' in method_source and
                                'len(h) > 2' in method_source and
                                'h[-2]' in method_source and
                                'h[-1]' in method_source
                            )
                        break

        if not method_found:
            print("Test 8 failed when checking TabManager.set_active_tab: method not found")
            return

        if not has_history_check:
            print("Test 8 failed when checking active tab history logic: history manipulation condition not found in set_active_tab")
            return

        print("Test 8 passed.")
    except Exception as e:
        print(f"Test 8 failed when reading tabs.py: {e}")


def test_9_history_pop_operations():
    """Test that TabManager.set_active_tab contains h.pop() operations"""
    try:
        content = read_file('kitty/tabs.py')
        tree = ast.parse(content)

        method_found = False
        pop_count = 0

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'TabManager':
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == 'set_active_tab':
                        method_found = True
                        method_source = ast.get_source_segment(content, item)

                        if method_source:
                            pop_count = method_source.count('h.pop()')
                        break

        if not method_found:
            print("Test 9 failed when checking TabManager.set_active_tab: method not found")
            return

        if pop_count < 2:
            print(f"Test 9 failed when checking history pop operations: found {pop_count} h.pop() calls, expected at least 2")
            return

        print("Test 9 passed.")
    except Exception as e:
        print(f"Test 9 failed when reading tabs.py: {e}")


def test_10_window_list_signature():
    """Test that WindowList.set_active_window_group_for has for_keep_focus parameter"""
    try:
        content = read_file('kitty/window_list.py')
        params = get_function_signature(content, 'WindowList', 'set_active_window_group_for')

        if params is None:
            print("Test 10 failed when checking WindowList.set_active_window_group_for method: method not found")
            return

        if 'for_keep_focus' not in params:
            print("Test 10 failed when checking set_active_window_group_for signature: for_keep_focus parameter missing")
            return

        # Check default value is None (allowing for trivial type annotation issues)
        default = params['for_keep_focus']
        if isinstance(default, ast.Constant):
            if default.value is not None:
                print(f"Test 10 failed when checking default value: expected None, got {default.value}")
                return

        print("Test 10 passed.")
    except Exception as e:
        print(f"Test 10 failed when reading window_list.py: {e}")


def test_11_active_group_history_logic():
    """Test that WindowList.set_active_window_group_for contains active group history manipulation logic"""
    try:
        content = read_file('kitty/window_list.py')
        tree = ast.parse(content)

        method_found = False
        has_history_check = False

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'WindowList':
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == 'set_active_window_group_for':
                        method_found = True
                        method_source = ast.get_source_segment(content, item)

                        if method_source:
                            has_history_check = (
                                'for_keep_focus' in method_source and
                                'len(h) > 2' in method_source and
                                'h[-2]' in method_source and
                                'h[-1]' in method_source
                            )
                        break

        if not method_found:
            print("Test 11 failed when checking WindowList.set_active_window_group_for: method not found")
            return

        if not has_history_check:
            print("Test 11 failed when checking active group history logic: history manipulation condition not found in set_active_window_group_for")
            return

        print("Test 11 passed.")
    except Exception as e:
        print(f"Test 11 failed when reading window_list.py: {e}")


def test_12_window_list_pop_operations():
    """Test that WindowList.set_active_window_group_for contains h.pop() operations"""
    try:
        content = read_file('kitty/window_list.py')
        tree = ast.parse(content)

        method_found = False
        pop_count = 0

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'WindowList':
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == 'set_active_window_group_for':
                        method_found = True
                        method_source = ast.get_source_segment(content, item)

                        if method_source:
                            pop_count = method_source.count('h.pop()')
                        break

        if not method_found:
            print("Test 12 failed when checking WindowList.set_active_window_group_for: method not found")
            return

        if pop_count < 2:
            print(f"Test 12 failed when checking history pop operations: found {pop_count} h.pop() calls, expected at least 2")
            return

        print("Test 12 passed.")
    except Exception as e:
        print(f"Test 12 failed when reading window_list.py: {e}")


if __name__ == "__main__":
    test_1_set_active_window_signature()
    test_2_set_active_tab_call_with_for_keep_focus()
    test_3_tab_set_active_window_call()
    test_4_launch_keep_focus_call()
    test_5_tab_set_active_window_signature()
    test_6_windows_set_active_window_group_for_call()
    test_7_tab_manager_set_active_tab_signature()
    test_8_active_tab_history_logic()
    test_9_history_pop_operations()
    test_10_window_list_signature()
    test_11_active_group_history_logic()
    test_12_window_list_pop_operations()
