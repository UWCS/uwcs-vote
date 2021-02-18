class PermsError:
    val = True

    @classmethod
    def suppress(cls):
        cls.val = False

    def __bool__(self):
        return self.val
