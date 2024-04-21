import flashcards
    
class Faculty:
    def __init__(self, fac):
        self.fac = fac

class Course(Faculty):
    def __init__(self, fac, cour):
        pass

class Group(Course):
    def __init__(self, fac, cour, gr):
        pass

class Student(Group):           # learning_materials -- карточки(другой файл)
    def __init__(self, fac, cour, gr, f_name, l_name, age, learning_materials):
        pass

class User(Student):
    def __init__(self, fac : Faculty, cour : Course, gr : Group, 
                 f_name : str, l_name : str, age : int, 
                 learning_materials : dict, friends : list):
        pass