class DomainModel:
    def __repr__name__(self) -> str:  # noqa: PLW3201
        return self.__class__.__name__

    def __repr__str__(self, separator: str) -> str:  # noqa: PLW3201
        props = (
            (name, getattr(self, name))
            for name, obj in self.__class__.__dict__.items()
            if isinstance(obj, property)
        )
        return separator.join(f'{k}={v!r}' for k, v in props)

    def __repr__(self) -> str:
        return f'{self.__repr__name__()}({self.__repr__str__(", ")})'
