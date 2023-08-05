# vyGeneric Library

### vyGenericObjectRepr
`from vyGeneric import vyGenericObjectRepr`
* vyGenericObjectRepr(object) will return nice printable 'repr' for your objects
* If you inherit your class, say 'MyClass', from vyGeneric, then any object of 
  MyClass, say 'myObject', prints all its hidden info when you call 
  print(myObject)

### vyGeneric
`from vyGeneric import vyGeneric`
* A generic class which uses vyGenericObjectRepr for repr

### vyGenericDict
`from vyGeneric import vyGenericDict`
* A descendant of vyGeneric which can store items like a dictionary

### vyGenericObjectRepr
`from vyGeneric import vyGenericArray`
* A descendant of vyGeneric which can store items like a list
