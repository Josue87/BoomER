import winreg

#Class to treat Windows Registry
class Registry():

    def __init__(self, key, subkey, value):
        self.key = key
        self.subkey = subkey
        self.value = str(value)
        self.current_key = None
	
    def _return_error(self, error):
	    return False, error
	
    def _return_success(self, ret):
        return True, ret
    
    def open_key(self, key, subkey):
        try:
            self.current_key = winreg.OpenKey(self.key, self.subkey, 0, winreg.KEY_WRITE)
            to_return = self._return_success(self.current_key)
        except Exception as e:
            to_return = self._return_error(str(e))
        return to_return

    def create_key(self):
        try:
            self.current_key = winreg.CreateKey(self.key, self.subkey)
            to_return = self._return_success(self.current_key)
        except WindowsError as e:
            to_return = self._return_error(str(e))
        return to_return
    
    def set_value(self):
        try:
            k = winreg.SetValue(self.key, self.subkey, winreg.REG_SZ, self.value)
            to_return = self._return_success(self.current_key)
        except WindowsError as e:
            to_return = self._return_error(str(e))
        return to_return
    
    def del_key(self):
        try:
            k =  winreg.DeleteKey(self.key, self.subkey)
            to_return = self._return_success(k)
            self.current_key = None
        except WindowsError as e:
            to_return = self._return_error(str(e))
        return to_return
    
    def start_process(self):
        success = True
        k = self.create_key()
        if k:
            v = self.set_value()
            if not v:
                print("Error setting value")
                success = False
        else:
            print("Key has not been created")
            success = False
        return success
    
    def restore_registry(self):
        k = self.del_key
        winreg.CloseKey(self.key)
        return k != None