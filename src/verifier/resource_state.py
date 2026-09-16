from dataclasses import dataclass


@dataclass
class ResourceState:

    resource_kind: str

    allocated: bool = False

    released: bool = False

    owner: str = None


    def allocate(self, owner=None):

        self.allocated = True
        self.released = False
        self.owner = owner


    def release(self):

        if not self.allocated:
            return False

        self.released = True
        self.allocated = False

        return True


    def is_live(self):

        return self.allocated and not self.released
