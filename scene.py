# -------------------------------------------------------------------- #
# scene.py
#   parent class for scene management
#	to change from one scene to another, do something like:
#	self.change_scene(ChildScene())
# -------------------------------------------------------------------- #

class Scene:
    def __init__(self):
        self.next = self

    def events(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def update(self, clock_tick):
        print("uh-oh, you didn't override this in the child class")

    def draw(self, screen, surface):
        print("uh-oh, you didn't override this in the child class")

    def change_scene(self, next_scene):
        self.next = next_scene

    def terminate(self):
        self.change_scene(None)
