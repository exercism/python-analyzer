shop = {
    # animal: (specie, descriptions)
    "parrot": ("Norvegian blue", ("restin'", "remarkable", "beautiful plumage")),
}

if "parrot" in shop and "restin'" in shop["parrot"][1]:
    print("Hellooooo, Pooolllllyyy ! WAAAAKEEY, WAKKEEEY !")


def xor_check(*, left=None, right=None):
    if (left is None) != (right is None):
        raise ValueError(
            "Either both left= and right= need to be provided or none should."
        )
