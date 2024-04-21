import random


class Flashcard:
    def __init__(self, subject : str, term : str, meaning : str):
        self.subject = subject
        self.term = term
        self.meaning = meaning
        
    def change(self, meaning : str):
        self.meaning = meaning

    def check_correct(self, term, meaning):
        return True if Flashcards.flashcards[term] == meaning else False
    






class Flashcards:
    def __init__(self, materials : dict) -> None:
        self.materials = materials



    def __str__(self) -> str:
        ret = ""
        for i in self.materials:
            ret += f"{i}\n"
        return ret

    def all_subjects(self):
        ret = ""
        for i in self.materials.keys():
            ret += f"{i}\n"
        return ret

    def all_s_flashcards(self, subject : str):
        ret = ""
        if self.check_subject(self, subject):
            ret = f"Flashcards in {subject}"
            for i in self.materials[subject]:
                ret += f"{i}\t"
        else:
            pass
        return ret



    def check_subject(self, subject : str) -> bool:
        return True if subject in self.materials.keys() else False

    def check_flashcard(self, subject : str, card : Flashcard) -> bool:
        if self.check_subject(self, subject):    
            return True if card in self.materials[subject] else False
        else: 
            return False



    def add_subject(self, subject : str):
        if not self.check_subject(self, subject):
            self.materials[subject] = []

    # def add_flashcard(self, subject : str, term : str, meaning : str):
    #     pass

    def add_flashcard(self, subject : str, card : Flashcard):
        flag = 0
        if self.check_subject(self, subject):
            for i in self.materials[subject]:
                if i.term == card.term:
                    i.meaning = card.meaning
                    flag =1
            if flag != 1:
                self.materials[subject].append(card)
        else:
            self.add_subject(self, subject)
            self.materials[subject].append(card)



    def change_subject(self, subject_old : str, subject_new : str):
        if self.check_subject(self, subject_old):
            self.materials[subject_new] = self.materials.pop(subject_old)
        else:
            pass

    def change_flashcard(self, subject : str, card_old : Flashcard, card_new : Flashcard):
        if (card_old.subject != card_new.subject):
            pass
        if self.check_subject(self, subject):
            for i in self.materials[subject]:
                if card_old.term == i.term:
                    i.term = card_new.term
                    i.meaning = card_new.meaning



    def delete_subject(self, subject : str):
        print(f"R u sure that u want to delete {subject}?")
        inp = input()
        if inp == "Yes":
            if self.check_subject(self, subject):
                self.materials.pop(subject)
                print(f"Deleted {subject}")
            else:
                pass


    def delete_flashcard(self, subject : str, term : str):
        pass



    def quiz(self, subject : str, mode = "meanings"):
        if (mode == "meanings"):
            if self.check_subject(self, subject):
                score = 0
                checking_list = self.materials[subject]
                random.shuffle(checking_list)
                for i in checking_list:
                    print(i.term)
                    inp = input()
                    if i.check_correct(self, i.term, inp):
                        print("Right!\n")
                        score += 1
                    else:
                        print(f"Mistake!\nAnswer: {i.meaning}\n")
                print(f"Score : {score}\n")
        elif (mode == "terms"):
            pass

        
    