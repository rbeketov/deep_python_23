import weakref
import time
import cProfile
import io
import pstats

from memory_profiler import profile
from prettytable import PrettyTable

class FirstAtributeObject:
    name_class = "FirstAtributeObject"
    def __init__(self,
                 number: int) -> None:
        self.number = {"Name": number,
                       "Surname": number + 1}


class SecondAtributeObject:
    name_class = "SecondAtributeObject"
    def __init__(self) -> None:
        self.number = ["Second", "atribute", "object", "this"]


class ThirdAtributeObject:
    name_class = "ThirdAtributeObject"
    def __init__(self,
                 number: str) -> None:
        self.number = number*10


class SimpleObject:
    def __init__(self,
                 obj_1: FirstAtributeObject,
                 obj_2: SecondAtributeObject,
                 obj_3: ThirdAtributeObject) -> None:
        self.object_1 = obj_1
        self.object_2 = obj_2
        self.object_3 = obj_3


class SlotsObject:
    __slots__ = ("object_1", "object_2", "object_3")
    def __init__(self,
                 obj_1: FirstAtributeObject,
                 obj_2: SecondAtributeObject,
                 obj_3: ThirdAtributeObject) -> None:
        self.object_1 = obj_1
        self.object_2 = obj_2
        self.object_3 = obj_3


class WeakrefObject:
    def __init__(self,
                 obj_1: FirstAtributeObject,
                 obj_2: SecondAtributeObject,
                 obj_3: ThirdAtributeObject) -> None:
        self.object_1 = weakref.ref(obj_1)
        self.object_2 = weakref.ref(obj_2)
        self.object_3 = weakref.ref(obj_3)


def processed_object_simple(obj, value):
    obj.object_1.number["Name"] = value
    obj.object_1.number["Surname"] = value + 1
    obj.object_1.name_class = str(value) + obj.object_1.name_class

    obj.object_2.number = [str(value), str(value+1), str(value+2)]
    obj.object_2.name_class = str(value) + obj.object_2.name_class

    obj.object_3.number = str(value)*10
    obj.object_3.name_class = str(value) + obj.object_3.name_class
    return obj


def processed_object_weakref(obj, value):
    obj.object_1().number["Name"] = value
    obj.object_1().number["Surname"] = value + 1
    obj.object_1().name_class = str(value) + obj.object_1().name_class

    obj.object_2().number = [str(value), str(value+1), str(value+2)]
    obj.object_2().name_class = str(value) + obj.object_2().name_class

    obj.object_3().number = str(value)*10
    obj.object_3().name_class = str(value) + obj.object_3().name_class
    return obj


def test_efficiency_time(class_: any,
                         num_iter: int,
                         num_object: int) -> None:
    # замер времени создания
    times_create = []
    for _ in range(num_iter):
        atribute_objects = [(FirstAtributeObject(i),
                             SecondAtributeObject(),
                             ThirdAtributeObject(str(i)))
                             for i in range(10_000, num_object+10_000)
        ]
        time_start = time.time()
        objects = [class_(first, second, third)
                   for first, second, third in atribute_objects
        ]
        time_end = time.time()
        times_create.append(time_end - time_start)
        for obj in objects:
            del obj
        for obj in atribute_objects:
            del obj
    times_create_mean = sum(times_create) / float(len(times_create))
    atribute_objects = [(FirstAtributeObject(i),
                         SecondAtributeObject(),
                         ThirdAtributeObject(str(i)))
                         for i in range(10_000, num_object+10_000)
    ]
    objects = [class_(first, second, third)
               for first, second, third in atribute_objects
    ]
    # замер времени чтения/изменения атрибутов
    times_edit = []
    
    if isinstance(objects[0], WeakrefObject):
        for start_pos in range(2_000, num_iter + 2_000): # избегаем кэшируемых объектов
            time_start = time.time()
            for i, obj in enumerate(objects, start=start_pos):
                obj = processed_object_weakref(obj, i)
            time_end = time.time()
            times_edit.append(time_end - time_start)
    else:
        for start_pos in range(2_000, num_iter + 2_000): # избегаем кэшируемых объектов
            time_start = time.time()
            for i, obj in enumerate(objects, start=start_pos):
                obj = processed_object_simple(obj, i)
            time_end = time.time()
            times_edit.append(time_end - time_start)

    times_edit_mean = sum(times_edit) / len(times_edit)
    return times_create_mean, times_edit_mean


@profile
def test_efficiency_memory(class_: any,
                           num_object: int):
    atribute_objects = [(FirstAtributeObject(i),
                         SecondAtributeObject(),
                         ThirdAtributeObject(str(i)))
                         for i in range(10_000, num_object+10_000)
    ]
    objects = [class_(first, second, third)
               for first, second, third in atribute_objects
    ]
    if isinstance(objects[0], WeakrefObject):
        for i, obj in enumerate(objects):
            obj = processed_object_weakref(obj, i)
    else:
        for i, obj in enumerate(objects):
            obj = processed_object_simple(obj, i)
        

def main():
    NUM_ITER = 10
    NUM_OBJECT = 1_000_000

    profiler = cProfile.Profile()

    profiler.enable()
    tcrete_simple, tedit_simple = test_efficiency_time(class_=SimpleObject, num_iter=NUM_ITER, num_object=NUM_OBJECT)
    tcrete_slots, tedit_slots = test_efficiency_time(class_=SlotsObject, num_iter=NUM_ITER, num_object=NUM_OBJECT)
    tcrete_weakref, tedit_weakref = test_efficiency_time(class_=WeakrefObject, num_iter=NUM_ITER, num_object=NUM_OBJECT)
    profiler.disable()

    test_efficiency_memory(class_=SimpleObject, num_object=NUM_OBJECT)
    test_efficiency_memory(class_=SlotsObject, num_object=NUM_OBJECT)
    test_efficiency_memory(class_=WeakrefObject, num_object=NUM_OBJECT)

    out = io.StringIO()
    stats = pstats.Stats(profiler, stream=out)
    stats.print_stats()

    table = PrettyTable()
    table.field_names = ["", "simple", "slots", "weakref"]
    table.add_row(["Время создания", f"{tcrete_simple:.2f}", f"{tcrete_slots:.2f}", f"{tcrete_weakref:.2f}"])
    table.add_row(["Время изменения/чтения", f"{tedit_simple:.2f}", f"{tedit_slots:.2f}", f"{tedit_weakref:.2f}"])
    print("======ВРЕМЕННЫЕ ЗАМЕРЫ======")
    print(f"Количество запусков: {NUM_ITER}")
    print(f"Количество экземпляров класса: {NUM_OBJECT}")
    print(table)

    print("======ПРОФИЛИРОВАНИЕ======")
    print(out.getvalue())


if __name__ == "__main__":
    main()
