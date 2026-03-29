class foo {
    + publicField: bool = True
    # protectedField: str = "default"
    - privateField: float = 3.14

    + publicMethod(param1: str): int
    # protectedMethod(param2: char): float
    - privateMethod(param3: str, param4: bool = False): void
}

function functfoo(param5: float, param6: int): void