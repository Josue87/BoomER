DATA_CHECK = {
        'screen' : {
          'command' : 'screen --version',
          'versions' : [{"4.05" : 'Privilege Escalation -> To get a RootShell try to run: exploit root_screen45'}],
          "os" : "linux",
          "description" : "Check app screen"
        },'kernel' : {
          'command' : 'uname -a',
          'versions' : [{"4.13" : 'Local Privilege Escalation'}, {"2.6.17.4": "Local Privilege Escalation"}],
          "os" : "linux",
          "description" : "Check kernel"
        },
        'jad' : {
          'command' : 'jad',
          'versions' : [{"1.5.8e" : 'Vulnerable to stack-based Buffer overflow'}],
          "os" : "linux",
          "description" : "Check app Jad"
        }
      }

EXPLOITS = {
        "root_screen45": {
          "function": "root_screen45",
          "os": "linux",
          "description": "Get a root shell exploiting vulnerability in 'Screen 4.5'"
        }
      }