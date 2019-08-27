global_variable_1 = 'global_variable'


class MyClass():
    class_var_1 = 'class_val_1'  # define class variable here

    def __init__(self, param):
        self.object_var_1 = param  # define object variable here
        self.object_var_2 = 'object_val_2'  # define object variable here
        self.object_func3()

    def object_func1(self, param):
        local_var_1 = param  # define lcoal variable here
        local_var_2 = 'local_val_2'  # define local variable here
        self.internal_var_1 = 'internal_val_1'  # define internal variable here
        print(local_var_1)  # we can use local variable of current here
        print(local_var_2)  # we can use local variable of current here
        print(MyClass.class_var_1)  # we can use class variable here, but you have using class name ass prefix
        print(self.class_var_1)  # we can use class variable as object variable here
        print(self.object_var_1)  # we can use object variable here
        print(self.object_var_2)  # we can use object variable here
        print(self.internal_var_1)  # we can use internal variable here
        # print(local_var_3) # we can't use local variable in another function
        print(global_variable_1)  # we can use global variable here

    def object_func2(self, param='func_val_1'):
        local_var_3 = param  # define local variable here
        print(local_var_3)  # we can use lcoal variable here
        print(
            self.internal_var_1)  # we can use internal variable defined in class_func1, but you have to call class_func1 first
        print(MyClass.class_var_1)  # we can use class variable here, but you have using class name ass prefix
        print(self.class_var_1)  # we can class variable here
        print(self.object_var_1)  # we can use object variable here
        print(self.object_var_2)  # we can use object variable here
        print(global_variable_1)  # we can use global variable here

    def object_func3(self, param='func_val_1'):
        self.object_var_3 = param  # because this function called in construction function, so this is defined as object variable, not internal variable
        self.object_var_4 = 'object_val_4'  # because this function called in construction function, so this is defined as object variable, not internal variable
        print(global_variable_1)  # we can use global variable here

    # define class function
    def class_func4():
        print(MyClass.class_var_1)
        print(global_variable_1)  # we can use global variable here


if __name__ == '__main__':
    myObject = MyClass('object_val_1')
    print(MyClass.class_var_1)  # we can use class variable directly here
    # print(MyClass.object_var_1) # we can't use object variable here
    print(myObject.object_var_1)  # we can use object variable here
    print(myObject.object_var_2)  # we can use object variable here
    print(myObject.object_var_3)  # we can use object variable here
    print(myObject.object_var_4)  # we can use object variable here
    # print(myObject.internal_var_1) # we can't use internal variable as object variable here
    MyClass.class_func4()  # we can use class function here
    # MyClass.object_func2(myObject, 'local_var_3') # internal variable can't be used in this function
    myObject.object_func1('local_var_1')  # call first function
    myObject.object_func2('local_var_3')  # call second function
    print(global_variable_1)  # we can use global variable here
