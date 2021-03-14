def total_effect() -> float:
    # TE = E[Y|do(X=1)] - E[Y|do(X=0)]
    raise NotImplementedError()  # TODO


def direct_effect() -> float:
    # DE = E[Y|do(X=x,Z=z)] - E[Y|do(X=x',Z=z)]
    raise NotImplementedError()  # TODO


def indirect_effect() -> float:
    raise NotImplementedError()  # TODO


def controlled_direct_effect() -> float:
    # CDE = E[Y|do(X=1,Z=z)] - E[Y|do(X=0,Z=z)]
    raise NotImplementedError()  # TODO


def natural_direct_effect() -> float:
    raise NotImplementedError()  # TODO


def natural_indirect_effect() -> float:
    raise NotImplementedError()  # TODO
