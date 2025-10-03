#!/usr/bin/env python3
"""
Test cases for commit c4c62c1505c48f90d75554f02030b76414637f8a
Testing changes related to --keep-focus flag and active history management
"""

import re


def read_file(filepath):
    """Read file content"""
    with open(filepath, 'r') as f:
        return f.read()


# Test 1: boss.py - set_active_window has for_keep_focus parameter
def test_1_set_active_window_signature():
    """Test that set_active_window method signature includes for_keep_focus parameter"""
    try:
        content = read_file('kitty/boss.py')
        # Look for the function definition with for_keep_focus parameter
        pattern = r'def set_active_window\(self,\s*window:\s*Window,\s*switch_os_window_if_needed:\s*bool\s*=\s*False,\s*for_keep_focus:\s*bool\s*=\s*False\)'

        if re.search(pattern, content):
            print("Test 1 passed.")
        else:
            print("Test 1 failed when checking set_active_window signature: for_keep_focus parameter not found in function definition")
    except Exception as e:
        print(f"Test 1 failed when reading boss.py: {e}")


# Test 2: boss.py - tm.set_active_tab called with for_keep_focus parameter
def test_2_set_active_tab_call_with_for_keep_focus():
    """Test that tm.set_active_tab is called with for_keep_focus parameter"""
    try:
        content = read_file('kitty/boss.py')
        # Look for tm.set_active_tab(tab, for_keep_focus=...)
        pattern = r'tm\.set_active_tab\(tab,\s*for_keep_focus='

        if re.search(pattern, content):
            print("Test 2 passed.")
        else:
            print("Test 2 failed when checking tm.set_active_tab call: for_keep_focus parameter not found in call")
    except Exception as e:
        print(f"Test 2 failed when reading boss.py: {e}")


# Test 3: boss.py - tab.set_active_window called with for_keep_focus parameter
def test_3_tab_set_active_window_call():
    """Test that tab.set_active_window is called with for_keep_focus parameter"""
    try:
        content = read_file('kitty/boss.py')
        # Look for tab.set_active_window(w, for_keep_focus=...)
        pattern = r'tab\.set_active_window\(w,\s*for_keep_focus='

        if re.search(pattern, content):
            print("Test 3 passed.")
        else:
            print("Test 3 failed when checking tab.set_active_window call: for_keep_focus parameter not found in call")
    except Exception as e:
        print(f"Test 3 failed when reading boss.py: {e}")


# Test 4: launch.py - boss.set_active_window called with for_keep_focus=True
def test_4_launch_keep_focus_call():
    """Test that boss.set_active_window is called with for_keep_focus=True in launch.py"""
    try:
        content = read_file('kitty/launch.py')
        # Look for boss.set_active_window(active, switch_os_window_if_needed=True, for_keep_focus=True)
        pattern = r'boss\.set_active_window\(active,\s*switch_os_window_if_needed=True,\s*for_keep_focus=True\)'

        if re.search(pattern, content):
            print("Test 4 passed.")
        else:
            print("Test 4 failed when checking launch.py: for_keep_focus=True not found in boss.set_active_window call")
    except Exception as e:
        print(f"Test 4 failed when reading launch.py: {e}")


# Test 5: tabs.py - Tab.set_active_window signature includes for_keep_focus parameter
def test_5_tab_set_active_window_signature():
    """Test that Tab.set_active_window method signature includes for_keep_focus parameter"""
    try:
        content = read_file('kitty/tabs.py')
        # Look for def set_active_window with for_keep_focus parameter
        pattern = r'def set_active_window\(self,\s*x:\s*Union\[Window,\s*int\],\s*for_keep_focus:\s*Optional\[Window\]\s*=\s*None\)'

        if re.search(pattern, content):
            print("Test 5 passed.")
        else:
            print("Test 5 failed when checking Tab.set_active_window signature: for_keep_focus parameter not found in function definition")
    except Exception as e:
        print(f"Test 5 failed when reading tabs.py: {e}")


# Test 6: tabs.py - windows.set_active_window_group_for called with for_keep_focus
def test_6_windows_set_active_window_group_for_call():
    """Test that windows.set_active_window_group_for is called with for_keep_focus parameter"""
    try:
        content = read_file('kitty/tabs.py')
        # Look for self.windows.set_active_window_group_for(x, for_keep_focus=...)
        pattern = r'self\.windows\.set_active_window_group_for\(x,\s*for_keep_focus='

        if re.search(pattern, content):
            print("Test 6 passed.")
        else:
            print("Test 6 failed when checking windows.set_active_window_group_for call: for_keep_focus parameter not found")
    except Exception as e:
        print(f"Test 6 failed when reading tabs.py: {e}")


# Test 7: tabs.py - TabManager.set_active_tab signature includes for_keep_focus
def test_7_tab_manager_set_active_tab_signature():
    """Test that TabManager.set_active_tab method signature includes for_keep_focus parameter"""
    try:
        content = read_file('kitty/tabs.py')
        # Look for def set_active_tab with for_keep_focus parameter
        pattern = r'def set_active_tab\(self,\s*tab:\s*Tab,\s*for_keep_focus:\s*Optional\[Tab\]\s*=\s*None\)'

        if re.search(pattern, content):
            print("Test 7 passed.")
        else:
            print("Test 7 failed when checking TabManager.set_active_tab signature: for_keep_focus parameter not found in function definition")
    except Exception as e:
        print(f"Test 7 failed when reading tabs.py: {e}")


# Test 8: tabs.py - Active tab history manipulation logic exists
def test_8_active_tab_history_logic():
    """Test that the active tab history manipulation logic is present"""
    try:
        content = read_file('kitty/tabs.py')
        # Look for the history manipulation logic in set_active_tab
        # Pattern for: if for_keep_focus and len(h) > 2 and h[-2] == for_keep_focus.id and h[-1] != for_keep_focus.id:
        pattern = r'if for_keep_focus and len\(h\) > 2 and h\[-2\] == for_keep_focus\.id and h\[-1\] != for_keep_focus\.id:'

        if re.search(pattern, content):
            print("Test 8 passed.")
        else:
            print("Test 8 failed when checking active tab history logic: history manipulation condition not found in set_active_tab")
    except Exception as e:
        print(f"Test 8 failed when reading tabs.py: {e}")


# Test 9: tabs.py - History pop operations exist
def test_9_history_pop_operations():
    """Test that h.pop() operations are present in set_active_tab"""
    try:
        content = read_file('kitty/tabs.py')
        # Look for the set_active_tab method and check for h.pop() calls
        set_active_tab_match = re.search(r'def set_active_tab\(self,.*?\n(?=    def |\Z)', content, re.DOTALL)

        if set_active_tab_match:
            method_content = set_active_tab_match.group(0)
            # Count h.pop() occurrences in the method
            pop_count = len(re.findall(r'\bh\.pop\(\)', method_content))
            if pop_count >= 2:
                print("Test 9 passed.")
            else:
                print(f"Test 9 failed when checking history pop operations: found {pop_count} h.pop() calls, expected at least 2")
        else:
            print("Test 9 failed when locating set_active_tab method")
    except Exception as e:
        print(f"Test 9 failed when reading tabs.py: {e}")


# Test 10: window_list.py - set_active_window_group_for signature includes for_keep_focus
def test_10_window_list_signature():
    """Test that set_active_window_group_for method signature includes for_keep_focus parameter"""
    try:
        content = read_file('kitty/window_list.py')
        # Look for def set_active_window_group_for with for_keep_focus parameter
        pattern = r'def set_active_window_group_for\(self,\s*x:\s*WindowOrId,\s*for_keep_focus:\s*Optional\[WindowType\]\s*=\s*None\)'

        if re.search(pattern, content):
            print("Test 10 passed.")
        else:
            print("Test 10 failed when checking set_active_window_group_for signature: for_keep_focus parameter not found in function definition")
    except Exception as e:
        print(f"Test 10 failed when reading window_list.py: {e}")


# Test 11: window_list.py - Active group history manipulation logic exists
def test_11_active_group_history_logic():
    """Test that the active group history manipulation logic is present in window_list.py"""
    try:
        content = read_file('kitty/window_list.py')
        # Look for the history manipulation logic in set_active_window_group_for
        pattern = r'if for_keep_focus and len\(h\) > 2 and h\[-2\] == for_keep_focus\.id and h\[-1\] != for_keep_focus\.id:'

        if re.search(pattern, content):
            print("Test 11 passed.")
        else:
            print("Test 11 failed when checking active group history logic: history manipulation condition not found in set_active_window_group_for")
    except Exception as e:
        print(f"Test 11 failed when reading window_list.py: {e}")


# Test 12: window_list.py - History pop operations in set_active_window_group_for
def test_12_window_list_pop_operations():
    """Test that h.pop() operations are present in set_active_window_group_for"""
    try:
        content = read_file('kitty/window_list.py')
        # Look for the set_active_window_group_for method
        method_match = re.search(r'def set_active_window_group_for\(self,.*?\n(?=    def |\Z)', content, re.DOTALL)

        if method_match:
            method_content = method_match.group(0)
            # Count h.pop() occurrences in the method
            pop_count = len(re.findall(r'\bh\.pop\(\)', method_content))
            if pop_count >= 2:
                print("Test 12 passed.")
            else:
                print(f"Test 12 failed when checking history pop operations: found {pop_count} h.pop() calls, expected at least 2")
        else:
            print("Test 12 failed when locating set_active_window_group_for method")
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
