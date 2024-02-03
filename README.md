Qt Type Formatters for LLDB
===========================

This project adds various [type formatters](https://lldb.llvm.org/use/variable.html#type-format)
to enable more user friendly display of Qt Core Types in LLDB and IDEs that
support it.

Usage
-----

Load the type formatters in LLDB by executing

```.console
command script import lldb_qt_formatters
```

or alternatively place the above line in a `.lldbinit` file in the root of the project, or in your `$HOME` directory.
To use a project-specific configuration file 
you will need to [enable it](https://lldb.llvm.org/man/lldb.html#configuration-files)

### VSCode

VSCode will not source a project `.lldbinit` file even if you enable it as above. To automatically load the
config file, add the following to your `launch.json` file.

```.json
"configurations": [{
    "type": "lldb",
    ...
    "initCommands": [
        "command source ${workspaceFolder}/.lldbinit"
    ]
}]

```

Supported Types
---------------

* `QMap<Key, Value>`
* `QMapNode<Key, Value>`
* `QString`


Contribution Guidelines
-----------------------

Contributions are welcomed.
See the guide to [variable formatting](https://lldb.llvm.org/use/variable.html) in LLDB, in addition to the
existing formatters in the [LLDB Source](https://github.com/llvm/llvm-project/tree/main/lldb/examples)

1. Create a test for your formatter. The tests run LLDB against some sample code and examine the formatted
   variable output.
2. Implement a new formatter
   * Simple types can be supported with a summary string in the `__init__.py` file
     (eg, see support for the `QMapNode<Key, Value>` type)
   * More complex types can be supported using the Python API (eg `QString`)
   * Container types such as `QMap<>` require more elaborate use of the Python API to generate *"Synthetic Children"*

   Formatters are registered with their types in the `__init__.py` file.
