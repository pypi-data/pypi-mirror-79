from __future__ import print_function
from .print import cformat, lformat


def findcaller(func):
    """
    查看调用者的文件位置路径和代码调用所在的行数，
    通过这种方式我可以一层一层的追踪代码执行的源头在哪里。
    也就是说一般使用它的场景是理解代码线性处理过程。
    """

    def wrapper(*args, **kwargs):
        import sys

        f = sys._getframe()
        filename = f.f_back.f_code.co_filename
        funcname = f.f_back.f_code.co_name

        lineno = f.f_back.f_lineno
        print(
            "{} {!s:<20} {} {} {} {} {}".format(
                cformat(func.__name__, fg="r"),
                " called by ",
                funcname,
                cformat(filename, fg="b"),
                cformat(lineno, fg="g"),
                args,
                kwargs,
            )
        )
        return func(*args, **kwargs)

    return wrapper


class ObjectAttrs(object):

    """
    一般用于调试某个对象时使用，当前这个工具类会将调试对象和其所属的所有继承对象的属性依次罗列出来。
    
    变量 showed_list 它是一个类变量, 用于记录已显示过的对象.
    
    使用方法:
    ObjectAttrs.show(调试对象)
    """

    showed_list = []

    @classmethod
    def show(cls, _class, show_attr=True, show_doc=False, _parent_class=None):
        """
        :param _class: 必填, 任意对象. 
        :param show_attr: 是否显示_class对象的所有attribute.                 
        :param show_doc: 是否显示_class对象的__doc__属性.
        :param _parent_class: 内部使用的参数, 用来传递_class对象的父类.                 
        :return: 
        """

        def _show(class_name):
            if class_name in cls.showed_list:
                return
            else:
                cls.showed_list.append(class_name)

            parent_class_name = (
                " inherited by {}".format(_parent_class) if _parent_class else ""
            )
            blank_lines = "\n" * 5 if show_attr else ""
            print(blank_lines, class_name, parent_class_name, sep="")

            if not show_attr:
                return

            for x in dir(class_name):
                if not show_doc:
                    if x == "__doc__":
                        continue
                try:
                    attr_name = x
                    attr_type = type(getattr(class_name, attr_name))
                    attr_object = getattr(class_name, attr_name)
                    print(
                        "{!s:<60}{!s:<60}{}".format(attr_name, attr_type, attr_object)
                    )
                except:
                    print("{!s:<60}{}".format(attr_name, "error"))

        _show(class_name=_class)

        parents = list(getattr(_class, "__bases__", ""))
        parents.append(getattr(_class, "__class__", ""))
        parents = [i for i in parents if i is not object and i is not type and i]

        for i in parents:
            cls.show(
                _class=i, _parent_class=_class, show_doc=show_doc, show_attr=show_attr
            )

