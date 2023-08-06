# pinlog
PinLog is a powerful driver and library integrated several logging systems. It is divided into smallest independent service units and easy to use.

## Installation

PinLog can be installed with [pip](http://pypi.python.org/pypi/pip):
    $ python -m pip install pinlog

## Get Start

#### Step 1 Import *pinlog*:
    >>> from pinlog import helper
    >>> from pinlog.log import Log
    >>> from pinlog.helper import Logger, Console, Logstash, Filters

#### Step 2 Add *@Logger* above the class
    >>> @Logger(Log.Console, Log.Logstash)
    >>> @Filters('username', 'firstname', 'middlename', 'lastname')
    >>> class MyClass():
    ... 
    ...     def __init__(self):
    ... 
    ... 

#### Step 3 Add *@Logger* above the class
    >>> mc = MyClass()
    >>> mc.pin('marker1')
    >>> time.sleep(3)
    >>> mc.pin('marker2')
    >>> print("--- %.8f seconds execution ---" % (mc.latency('marker1', 'marker2')))
    --- 3.00161195 seconds execution ---

Moreover, you can trace anywhere even if across the applications as below examples

### Example of tracing over 2 applications
#### *class1.py* The first application:
    from pinlog import helper
    from pinlog.log import Log
    from pinlog.helper import Logger, Console, Logstash, Filters
    import time

    @Logger(Log.Console, Log.Logstash)
    @Filters('username', 'firstname', 'middlename', 'lastname')
    class Class1():
        
        def __init__(self):
            pass

        def function1(self, str):
            pass


    c1 = Class1()
    c1.pin('marker1')
    time.sleep(3)
    c1.pin('marker2')

#### *class2.py* The second application:
    from pinlog import helper
    from pinlog.log import Log
    from pinlog.helper import Logger, Console, Logstash, Filters

    @Logger(Log.Console, Log.Logstash)
    class Class2():

        def __init__(self):
            pass

        def function2(self, str):
            pass

    c2 = Class2()
    data = {
        'username': 'admin',
        'password': '1qazxsw2',
        'firstname': 'Tom',
        'lastname': 'Cruise',
        'role': 'Administrator',
        'birthdate': 'July 3, 1962',
        'department': 'Cruise/Wagner Productions'
    }
    output1 = c2.trace('marker1', data)
    print('Output 1 : ', output1)
    output2 = c2.trace('marker2', data)
    print('Output 2 : ', output2)

#### Output:
    Output 1 : {'username': 'admin', 'firstname': 'Tom', 'middlename': None, 'lastname': 'Cruise', 'latency': 13.845938920974731}
    Output 2 : {'username': 'admin', 'firstname': 'Tom', 'middlename': None, 'lastname': 'Cruise', 'latency': 10.844847202301025}