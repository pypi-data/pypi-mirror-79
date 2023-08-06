import fire
from donno import notes


class App:
    def add(self):
        '''Add a new note in the current notebook'''
        notes.add_note()

    def a(self):
        """Alias of add command"""
        self.add()

    def delete(self, no):
        notes.delete_note(no)

    def list(self, number=5):
        '''List most updated <number> notes'''
        print(notes.list_notes(number))

    def l(self, number=5):  # noqa
        """Alias of list command"""
        self.list(number)

    def edit(self, no=1):
        notes.update_note(no)

    def e(self, no=1):
        '''Alias of edit command'''
        self.edit(no)

    def search(self, *keys):
        print(notes.simple_search(keys))

    def s(self, *keys):
        '''alias for search command'''
        self.search(*keys)

    def view(self, no=1):
        notes.view_note(no)

    def v(self, no=1):
        '''Alias of view command'''
        self.view(no)


def main():
    fire.Fire(App)


# for test purpose:
# python donno/app.py s python con
if __name__ == '__main__':
    main()
